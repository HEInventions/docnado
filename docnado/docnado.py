""" docnado.py

A rapid documentation tool that will blow you away.

"""

import os
import re
import sys
import csv
import glob
import time
import signal
import shutil
import urllib
import base64
import hashlib
import argparse
import tempfile
import datetime
import threading
import traceback
import subprocess
import platform
import requests

from bs4 import BeautifulSoup

from multiprocessing import Pool

from urllib.parse import urlparse

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import timeago
from xml.etree import ElementTree
from flask import Flask, url_for, abort, send_from_directory, \
    render_template, Markup, make_response, render_template_string

import markdown
import markdown.util
from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from markdown.inlinepatterns import LinkPattern, IMAGE_LINK_RE, dequote, handleAttributes
from markdown.blockprocessors import HashHeaderProcessor

from http.client import responses

if __package__:
    from .navtree import NavItem, parse_nav_string
else:
    from navtree import NavItem, parse_nav_string


class MultiPurposeLinkPattern(LinkPattern):
    """ Embed image, video, youtube, csv or file download links
    by extending the typical image tag pattern.

    # ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)

    If the link has "DOWNLOAD" in the alt text, treat it as a download.
    Otherwise, see if its a YouTube video.  Otherwise, see if its a
    csv that can be turned into a table, otherwise if the link cannot be parsed
    as a video, it will always be treated as an image.
    """
    SUPPORTED_VIDEO = ('ogv', 'ogg', 'avi', 'mp4', 'webm', )
    SUPPORTED_TABLES = ('csv', )
    SUPPORTED_PDF = ('pdf', )

    def get_src(self, m):
        """ Get the source and parts from the matched groups: src, parts """
        src_parts = m.group(9).split()
        if src_parts:
            src = src_parts[0]
            if src[0] == "<" and src[-1] == ">":
                src = src[1:-1]
            return self.sanitize_url(self.unescape(src)), src_parts

        else:
            return '', src_parts

    @staticmethod
    def youtube_url_validation(url):
        """ Given a YouTube URL, return the ID component.
        https://stackoverflow.com/questions/4705996
        """
        youtube_regex = (r'(https?://)?(www\.)?'
                         r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
                         r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_match = re.match(youtube_regex, url)
        return youtube_regex_match.group(6) if youtube_regex_match else None

    @staticmethod
    def as_youtube(m, video_id):
        """ Return a DOM element that embeds a YouTube video. """
        el = ElementTree.Element('iframe')
        el.set('class', 'video')
        el.set('src', f'https://www.youtube.com/embed/{video_id}?rel=0')
        el.set('frameborder', '0')
        el.set('allow', 'autoplay; encrypted-media')
        el.set('allowfullscreen', '1')
        return el

    def as_pdf(self, m):
        """ Return a DOM element that embeds a PDF document using an embed. """
        src, parts = self.get_src(m)

        wrapper = ElementTree.Element('aside')
        wrapper.set('class', 'pdf-embed-wrapper')

        el = ElementTree.SubElement(wrapper, 'embed')
        el.set('class', 'pdf-embed')
        el.set('src', src)
        el.set('width', '100%')
        el.set('type', 'application/pdf')
        el.set('height', '100%')  # width * 1.4142 (aspect ratio of a4)
        el.set('pluginspage', 'http://www.adobe.com/products/acrobat/readstep2.html')
        if len(parts) > 1:
            el.set('alt', dequote(self.unescape(" ".join(parts[1:]))))
        return wrapper

    def as_video(self, m):
        """ Return a video element """
        src, parts = self.get_src(m)
        el = ElementTree.Element('video')
        el.set('src', src)
        el.set("controls", "true")
        handleAttributes(m.group(2), el)
        return el

    def as_image(self, m):
        """ Return an image element """
        el = ElementTree.Element('img')
        src, parts = self.get_src(m)
        el.set('src', src)

        # Set the title if present.
        if len(parts) > 1:
            el.set('title', dequote(self.unescape(" ".join(parts[1:]))))

        # Set the attributes on the element, if enabled.
        # Set the 'alt' attribute with whatever is left from `handleAttributes`.
        attrs = self.markdown.enable_attributes
        alt_text = handleAttributes(m.group(2), el) if attrs else m.group(2)
        el.set('alt', self.unescape(alt_text))
        return el

    def as_csv(self, m):
        src, parts = self.get_src(m)
        root = ElementTree.Element('table')
        root.set('source', src)
        root.set('class', 'csv-table table thead-light table-hover')
        file_path = os.path.join(self.markdown.page_root, src)
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = [r for r in reader]
            thead = ElementTree.SubElement(root, 'thead')
            for col in headers:
                ElementTree.SubElement(thead, 'th').text = col
            for row in rows:
                tr = ElementTree.SubElement(root, 'tr')
                for col in row:
                    ElementTree.SubElement(tr, 'td').text = col
        return root

    def as_download(self, m):
        """ Create card layers used to make a download button. """
        src, parts = self.get_src(m)

        # Returns a human readable string representation of bytes
        def _human_size(byte_number, units=(' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB')):
            return str(byte_number) + units[0] if byte_number < 1024 else _human_size(byte_number >> 10, units[1:])

        # Get information required for card.
        split_src = os.path.split(src)
        file_path = os.path.join(self.markdown.page_root, *split_src)
        file_size = os.path.getsize(file_path)
        file_basename = os.path.basename(file_path)
        card_text = dequote(self.unescape(" ".join(parts[1:]))) if len(parts) > 1 else ''

        # If its a pptx, extract the thumbnail previews.
        # NOTE: This works, but is is removed until we support other
        # file types, which for now is not a priority.
        # preview_uri = None
        # import zipfile
        # if (file_path.endswith('pptx')):
        #     with zipfile.ZipFile(file_path) as zipper:
        #         with zipper.open('docProps/thumbnail.jpeg', 'r') as fp:
        #             mime = 'image/jpeg'
        #             data64 = base64.b64encode(fp.read()).decode('utf-8')
        #             preview_uri = u'data:%s;base64,%s' % (mime, data64)

        # Card and structure.
        card = ElementTree.Element("div")
        card.set('class', 'card download-card')
        header = ElementTree.SubElement(card, 'div')
        header.set('class', 'download-card-header')
        body = ElementTree.SubElement(card, 'div')
        body.set('class', 'download-card-body')

        # Add preview image.
        # if preview_uri:
        #     img = ET.SubElement(header, 'img')
        #     img.set('src', preview_uri)

        # Filename link heading.
        heading = ElementTree.SubElement(body, 'a')
        heading.set('class', 'download-card-title')
        heading.set('href', src)
        download_icon = ElementTree.SubElement(heading, 'i')
        download_icon.set('class', 'fa fa-download')
        download_text = ElementTree.SubElement(heading, 'span')
        download_text.text = file_basename

        # Title element from the "quote marks" part.
        body_desc = ElementTree.SubElement(body, 'span')
        body_desc.text = card_text

        # File size span at the bottom.
        body_size = ElementTree.SubElement(body, 'span')
        body_size.set('class', 'small text-muted')
        body_size.text = f'{_human_size(file_size)}'
        return card

    @staticmethod
    def _is_inject(m):
        """ Determine if the ALT text [] part of the link says 'INJECT'. """
        alt = m.group(2)
        return alt.lower() == 'inject'

    def as_raw(self, m):
        """ Load the HTML document specified in the link, parse it to HTML elements and return it.
        """
        src, parts = self.get_src(m)

        # Find the path to the HTML document, relative to the current markdown page.
        file_path = os.path.join(self.markdown.page_root, src)
        raw_html_string = read_html_for_injection(file_path)

        if len(parts) < 2:
            parts.append("nothing_one=1||nothing_two=2")

        # Helper function.
        def _argify(args):
            if '=' not in args:
                raise ValueError('injection template requires named arguments split by ||')
            left, right = args.split('=')
            return left.strip(), right.strip()

        # Split arg string on double pipe. Joins them to undo automattic splitting from the markdown.
        arg_strings = " ".join(parts[1:]).strip('\"').split("||")

        # Parse into dictionary of key-value pairs based on the '=' notation.
        try:
            named_args = dict([_argify(args) for args in arg_strings])
        except Exception as e:
            raise Exception(f"Error parsing ![INJECT] arguments in {self.markdown.page_file} {repr(e)}")

        # Take the template renderer and give it our string, and named args.
        # Capture the output as a string.
        try:
            injectable_templated_str = render_template_string(raw_html_string, **named_args)
        except Exception as e:
            raise Exception(f"Error rendering ![INJECT] template for file {file_path} {repr(e)}")

        # Feed that string to the XML parser.
        try:
            return ElementTree.fromstring(injectable_templated_str)
        except Exception as e:
            raise Exception(f"Error parsing ![INJECT] template for file {file_path} {repr(e)}")

    @staticmethod
    def _is_download(m):
        """ Determine if the ALT text [] part of the link says 'DOWNLOAD'. """
        alt = m.group(2)
        return alt.lower() == 'download'

    def handleMatch(self, m):
        """ Use the URL extension to render the link. """
        src, parts = self.get_src(m)
        if self._is_download(m):
            return self.as_download(m)

        elif self._is_inject(m):
            return self.as_raw(m)

        youtube = self.youtube_url_validation(src)
        if youtube:
            return self.as_youtube(m, youtube)

        src_lower = src.lower()
        if src_lower.endswith(self.SUPPORTED_TABLES):
            return self.as_csv(m)

        elif src_lower.endswith(self.SUPPORTED_PDF):
            return self.as_pdf(m)

        elif src_lower.endswith(self.SUPPORTED_VIDEO):
            return self.as_video(m)

        return self.as_image(m)


class OffsetHashHeaderProcessor(HashHeaderProcessor):
    """ Process hash headers with an offset to control the type of heading
    DOM element that is generated. """

    HEADING_LEVEL_OFFSET = 1

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[:m.start()]
            after = block[m.end():]
            if before:
                self.parser.parseBlocks(parent, [before])
            heading_level = len(m.group('level'))
            h = ElementTree.SubElement(parent, 'h%d' % (heading_level + self.HEADING_LEVEL_OFFSET))
            h.text = m.group('header').strip()
            if after:
                blocks.insert(0, after)


class ChecklistPostprocessor(Postprocessor):
    """
    Adds checklist class to list element.
    Adapted from: `markdown_checklist.extension`
    """
    pattern = re.compile(r'<li>\[([ Xx])\]')

    def run(self, html):
        html = re.sub(self.pattern, self._convert_checkbox, html)
        before = '<ul>\n<li><input type="checkbox"'
        after = before.replace('<ul>', '<ul class="checklist">')
        html = html.replace(before, after)
        return html

    @staticmethod
    def _convert_checkbox(match):
        state = match.group(1)
        checked = ' checked' if state != ' ' else ''
        return '<li><input type="checkbox" disabled%s>' % checked


# Remove the `video`, `iframe`, `aside`, and `table` elements as block elements.
markdown.util.BLOCK_LEVEL_ELEMENTS = re.compile(
    r"^(p|div|h[1-6]|blockquote|pre|dl|ol|ul"
    r"|script|noscript|form|fieldset|math"
    r"|hr|hr/|style|li|dt|dd|thead|tbody"
    r"|tr|th|td|section|footer|header|group|figure"
    r"|figcaption|article|canvas|output"
    r"|progress|nav|main)$",
    re.IGNORECASE
)


class MultiExtension(Extension):
    """ Markdown `Extension` that adds our new components and
    overrides some that we are not using.
    """
    def extendMarkdown(self, md, md_globals):
        """ Configure markdown by disabling elements and replacing them with
        others. """
        # Add checklist processing extension based on: 'markdown_checklist.extension'.
        md.postprocessors.add('checklist', ChecklistPostprocessor(md), '>raw_html')

        # Remove default patterns.
        del md.inlinePatterns['image_link']

        # Create a new one and insert into pipeline.
        multi_purpose_pattern = MultiPurposeLinkPattern(IMAGE_LINK_RE, md)
        md.inlinePatterns['multi_purpose_pattern'] = multi_purpose_pattern

        # Remove line headers.
        del md.parser.blockprocessors['setextheader']

        # Swap hash headers for one that can change the DOM h1, h2 level.
        md.parser.blockprocessors['hashheader'] = OffsetHashHeaderProcessor(md.parser)


# https://python-markdown.github.io/extensions/
mdextensions = [MultiExtension(),
                'markdown.extensions.tables',
                'markdown.extensions.meta',
                'markdown.extensions.def_list',
                'markdown.extensions.headerid',
                'markdown.extensions.fenced_code',
                'markdown.extensions.attr_list']


def build_meta_cache(root):
    """ Recursively search for Markdown files and build a cache of `Meta`
    from metadata in the Markdown.
    :param root: str: The path to search for files from.
    """
    doc_files = glob.iglob(root + '/**/*.md', recursive=True)

    def _meta(path):
        with open(path, 'r', encoding='utf-8') as f:
            md = markdown.Markdown(extensions=mdextensions)
            md.page_root = os.path.dirname(path)
            Markup(md.convert(f.read()))
            return md.Meta if hasattr(md, 'Meta') else None

    doc_files_meta = {os.path.relpath(path, start=root): _meta(path) for path in doc_files}
    doc_files_meta = {path: value for path, value in doc_files_meta.items() if value is not None}

    # If a nav filter is set, exclude relevant documents.
    # This takes the comma separated string supplied to `nav_limit`
    # and excludes certain documents if they are NOT in this list.
    global CMD_ARGS
    if CMD_ARGS.nav_limit:
        nav_filters = CMD_ARGS.nav_limit.split(',')
        nav_filters = [nav_filter.strip().lower() for nav_filter in nav_filters]
        nav_filters = [nav_filter for nav_filter in nav_filters if nav_filter]

        def _should_include(doc_meta):
            nav_strings = [nav.lower() for nav in doc_meta.get('nav', [])]
            return any([y.startswith(x) for x in nav_filters for y in nav_strings])
        doc_files_meta = {path: value for path, value in doc_files_meta.items() if _should_include(value)}

    return doc_files_meta


def build_nav_menu(meta_cache):
    """ Given a cache of Markdown `Meta` data, compile a structure that can be
    used to generate the NAV menu.
    This uses the `nav: Assembly>Bench>Part` variable at the top of the Markdown file.
    """
    root = NavItem('root', 0)

    # Pre-sort the nav-items alphabetically by nav-string. This will get overridden with the arange()
    # function, but this avoids-un arranged items moving round between page refreshes due to Dicts being 
    # unordered.
    sorted_meta_cache = sorted(
        meta_cache.items(),
        key = lambda items: items[1].get('nav', [''])[0].split('>')[-1] # Sort by the last part of the nav string for each page.
        )

    for path, meta in sorted_meta_cache:
        nav_str = meta.get('nav', [None])[0]
        nav_chunks = parse_nav_string(nav_str)
        node = root
        for name, weight in nav_chunks:
            n = NavItem(name, weight)
            node = node.add(n)
        node.bind(meta=meta, link=path)
    root.arrange()
    return root


def build_reload_files_list(extra_dirs):
    """ Given a list of directories, return a list of files to watch for modification
    and subsequent server reload. """
    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = os.path.join(dirname, filename)
                if os.path.isfile(filename):
                    extra_files.append(filename)
    return extra_files

def read_html_for_injection(path):
    """ Open an HTML file at the given path and return the contents
    as a string.  If the file does not exist, we raise an exception.
    """
    # TODO: In the future, consider adding some caching here.  However,
    # beware of reloading / refereshing the page UX implications.
    with open(path) as file:
        return file.read()

def _render_markdown(file_path, **kwargs):
    """ Given a `file_path` render the Markdown and return the result of `render_template`.
    """
    global NAV_MENU, PROJECT_LOGO, PDF_GENERATION_ENABLED
    default_template = 'document'
    with open(file_path, 'r', encoding='utf-8') as f:
        md = markdown.Markdown(extensions=mdextensions)
        md.page_root = os.path.dirname(file_path)
        md.page_file = file_path
        markup = Markup(md.convert(f.read()))

        # Fetch the template defined in the metadata.
        template = md.Meta.get('template', None)
        template = template[0] if template else default_template
        if not template:
            raise Exception('no template found for document')
        template = f'{template}.html'

        # Load any HTML to be injected from the meta-data.
        injections = md.Meta.get('inject', [])
        injections = [os.path.join(md.page_root, file) for file in injections]
        injections = [read_html_for_injection(file) for file in injections]

        # Render it out with all the prepared data.
        return render_template(template,
                               content=markup,
                               nav_menu=NAV_MENU,
                               project_logo=PROJECT_LOGO,
                               pdf_enabled=PDF_GENERATION_ENABLED,
                               injections=injections,
                               **md.Meta,
                               **kwargs)


def configure_flask(app, root_dir):
    """ Setup the flask application within this scope. """

    @app.before_first_request
    def build_navigation_cache():
        """  Build an in-memory cache of document meta-data.
        NOTE: The design choice is made to crash the application if any
        of the markdown files cannot be opened and parsed. In the
        future when it becomes more stable, this will probably change.
        """
        # This is called each time the server restarts.
        global NAV_MENU
        meta_cache = build_meta_cache(root_dir)

        # Build the nav menu data-structure.
        NAV_MENU = build_nav_menu(meta_cache)

    # Store the reference to the function that rebuilds the navigation cache.
    app.build_navigation_cache = build_navigation_cache

    @app.template_filter('gravatar')
    def gravatar(email, size=100, rating='g', default='retro', use_ssl=False):
        """ Return a gravatar link for a given email address. """
        url = "https://secure.gravatar.com/avatar/" if use_ssl else "http://www.gravatar.com/avatar/"
        email = email.strip().lower().encode('utf-8')
        hash_email = hashlib.md5(email).hexdigest()
        return f'{url}{hash_email}?s={size}&r={rating}&d={default}'

    @app.template_filter()
    def timesince(dt, past_="ago", future_="from now", default="just now"):
        """ Returns string representing "time since" e.g. 3 days ago, 5 hours ago etc.
        :param str dt Input date string in the format %Y/%m/%d
        http://flask.pocoo.org/snippets/33/
        """
        try:
            dt = datetime.datetime.strptime(dt, '%Y/%m/%d')
            return_value = timeago.format(dt, datetime.datetime.utcnow())
            return return_value
        except:
            print('ERROR: Could not parse date string.')
            sys.exit(-1)


    @app.template_filter()
    def url_unquote(url):
        """ Removes encoding around a URL. """
        return urllib.parse.unquote(url)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route("/print_header")
    def print_header():
        """ Render the template for the header used when printing with WKPDFTOHTML. """
        global PROJECT_LOGO
        return render_template('print_header.html', project_logo=PROJECT_LOGO)

    @app.route("/print_footer")
    def print_footer():
        """ Render the template for the footer used when printing with WKPDFTOHTML. """
        global PROJECT_LOGO
        return render_template('print_footer.html', project_logo=PROJECT_LOGO)

    @app.errorhandler(404)
    def page_not_found(e):
        global NAV_MENU, PROJECT_LOGO
        return render_template('404.html', nav_menu=NAV_MENU, project_logo=PROJECT_LOGO), 404

    @app.route("/w/<path:page>")
    def wiki(page):
        """ Render the page. """
        file_path = os.path.abspath(os.path.join(root_dir, page))
        if not os.path.isfile(file_path):
            abort(404)

        if '.md' in [ext.lower() for ext in os.path.splitext(file_path)]:
            return _render_markdown(file_path, current_page=page)
        else:
            return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))

    @app.route("/")
    @app.route("/w/")
    def homepage():
        return wiki('home.md')

    @app.route("/pdf/<path:page>")
    def wiki_pdf(page):
        file_path = os.path.abspath(os.path.join(root_dir, page))
        if not os.path.isfile(file_path):
            abort(404)

        if '.md' not in [ext.lower() for ext in os.path.splitext(file_path)]:
            return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))

        # Configure the different paths.
        pdf_temp = f'{tempfile.mktemp()}.pdf'
        input_url = url_for('wiki', page=page, _external=True)
        header_url = url_for('print_header', _external=True)
        footer_url = url_for('print_footer', _external=True)
        args = f'{WKHTMLTOPDF_BINARY} --header-html {header_url} --footer-html {footer_url} \
                --print-media-type --header-spacing 2  {input_url} {pdf_temp}'

        # Invoke WkHTMLtoPDF
        result = subprocess.check_output(args, shell=True)
        if not result:
            pass

        # Write the newly generated temp pdf into a response.
        with open(pdf_temp, 'rb') as f:
            binary_pdf = f.read()
            target_file_name = page.replace("/", "_").replace("\\", "_")
            response = make_response(binary_pdf)
            response.headers['Content-Type'] = 'application/pdf'
            # response.headers['Content-Disposition'] = f'attachment; filename={target_file_name}.pdf'
            response.headers['Content-Disposition'] = f'inline; filename={target_file_name}.pdf'

        # Delete the temp file and return the response.
        os.remove(pdf_temp)
        return response


def generate_static_pdf(app, root_dir, output_dir, nav_filter=None):
    """ Generate a static PDF directory for the documentation in `root_dir`
    into `output_dir`.
    """
    global PORT_NUMBER
    # Find all markdown document paths that are in the nav.
    documents = build_meta_cache(root_dir)
    markdown_docs_urls = ['pdf/' + file.replace('\\', '/') for file in documents.keys()]

    # Generate URl to file pairs.
    pairs = [(f'http://localhost:{PORT_NUMBER}/{url}',
             f'{os.path.join(output_dir, *os.path.split(url))}.pdf')
             for url in markdown_docs_urls]

    # Download each pair.
    for source, target in pairs:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        print(f'Source: {source} \n Target: {target}')
        urllib.request.urlretrieve(source, target)


# Helper function to return the domain if present.
def is_absolute(url):
    """ Returns True if the passed url string is an absolute path.
        False if not
    """
    links = urlparse(url)

    return bool(links.netloc)


def generate_static_html(app, root_dir, output_dir):
    """ Generate a static HTML site for the documentation in `root_dir`
    into `output_dir`.
    """
    from flask_frozen import Freezer, MissingURLGeneratorWarning
    import warnings
    warnings.filterwarnings("ignore", category=MissingURLGeneratorWarning)

    # Update the flask config.
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
    app.config['FREEZER_DESTINATION'] = output_dir

    # Create the freezer app.  Make it use specific URLs.
    freezer = Freezer(app, with_no_argument_rules=False, log_url_for=False)

    # Register a generator that passes ALL files in the docs directory into the
    # `wiki` flask route.
    @freezer.register_generator
    def wiki():
        all_docs = [file.replace(f'{root_dir}', '/w').replace(f'{os.path.sep}', '/')
                    for file in glob.iglob(f'{root_dir}/**/*', recursive=True)
                    if os.path.isfile(file)]
        for doc in all_docs:
            yield doc

    # Save all the URLs using the correct extension and MIME type.
    freezer.freeze()

    # For each `.md` file in the output directory:
    for markdown_file in glob.iglob(f'{output_dir}/**/*.md', recursive=True):

        # Rewrite all relative links to other `.md` files to `.html.`
        output = ''
        with open(markdown_file, 'r', encoding="utf-8") as f:
            html = f.read()

            def _href_replace(m):
                href = m.group()
                if is_absolute(href[6:-1]):
                    return href
                return href.replace('.md', '.html')

            output = re.sub('href="(.*md)"', _href_replace, html)

        # Rename the file from `.md` to HTML.
        with open(markdown_file[:-3] + '.html', 'w', encoding="utf-8") as f:
            f.write(output)

        # Delete the Markdown file.
        os.remove(markdown_file)


def load_project_logo(logo_file=None):
    """ Attempt to load the project logo from the specified path.
    If this fails, return None.  If this succeeds, convert it to a data-uri.
    """
    if not logo_file:
        return None
    if not os.path.exists(logo_file):
        return None
    with open(logo_file, 'rb') as fp:
        mime = 'image/png'
        data64 = base64.b64encode(fp.read()).decode('utf-8')
        preview_uri = u'data:%s;base64,%s' % (mime, data64)
        return preview_uri


def check_pdf_generation_cap():
    """ Check to see if we can use PDF generation by attempting to use the binary. """
    global WKHTMLTOPDF_BINARY
    retcode = subprocess.call(f'{WKHTMLTOPDF_BINARY} --version',
                              shell=True,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    return retcode == 0


def copy_local_project(force=False):
    """ Copy the sample docs and style into the local working directory.
    Note: This will overwrite anything currently in those folders.
    """
    source_root = os.path.dirname(__file__)
    target_root = os.getcwd()

    targets = ['docs', 'style', 'logo.png']
    pairs = [(os.path.join(source_root, path), os.path.join(target_root, path))
             for path in targets]

    for source, target in pairs:
        if os.path.isdir(source):
            if os.path.exists(target):
                if force:
                    print(f'Deleting existing {target} and replacing it with {target}')
                    shutil.rmtree(target)
                    shutil.copytree(source, target)
                else:
                    print(f'Warning: {target} already exists.')
            else:
                print(f'Copying: {source} -> {target}')
                shutil.copytree(source, target)
        else:
            if os.path.exists(target):
                if force:
                    print(f'Deleting existing {target} and replacing it with {target}')
                    os.remove(target)
                    shutil.copyfile(source, target)
                else:
                    print(f'Warning: {target} already exists.')
            else:
                print(f'Copying: {source} -> {target}')
                shutil.copyfile(source, target)


def find_references(document_path):
    """ Search through the markdown 'document_path' and make a list of referenced files
    with paths that are relative to the directory containing the `document_path`.
    """
    # Open the file to search.
    with open(document_path, 'r', encoding='utf-8') as f:
        markdown_raw_data = f.read()

    # Render as HTML.
    md = markdown.Markdown(extensions=mdextensions)
    document_dir = os.path.dirname(document_path)
    md.page_root = document_dir

    # Interpret with the BeautifulSoup HTML scraping library.
    soup = BeautifulSoup(md.convert(markdown_raw_data), 'html.parser')
    tags_to_search = {
        'img': 'src',
        'a': 'href',
        'video': 'src',
        'table': 'source',
        'embed': 'src',
    }

    # For each entry in the `tags_to_search` table, extract the tag attribute value.
    references = set()
    for k, v in tags_to_search.items():
        for tag in soup.find_all(k):
            val = tag.get(v)
            if val:
                references.add(val)

    # Normalise the referenced assets (to take into account relative paths).
    references = [os.path.join(document_dir, urllib.request.url2pathname(ref)) for ref in references]

    # Make unique.
    return set(references)


def has_nav(markdown_text):
    """ Returns True if the passed string of text contains navbar metadata.
        Returns False if it does not.
    """
    expression = re.compile(r'(?=\n|)nav:\s+\w+(?=\n |)')
    return True if expression.search(markdown_text) else False


def find_orphans(files):
    """ Searches all files and folders recursively in the given path for image and video assets
        that are unused by markdown files.
    """
    # Find all references in
    pages = {}
    for file in files:
        if file.endswith('.md'):
            pages[file] = find_references(file)

    # Remove the markdown documents that have a navbar metadata.
    md_with_nav = []
    for file in files:
        if file.endswith('.md'):
            with open(file, encoding='utf-8') as f:
                if has_nav(f.read().lower()):
                    md_with_nav.append(file)

    files = [x for x in files if x not in md_with_nav]

    # Create a flat list of all references in the markdown files
    all_references = []
    for i in pages.values():
        all_references += [k for k in i]

    # Output unused assets
    return [i for i in files if i not in all_references]


class DocumentLinks:
    """ A helper class to process the `<a href.../>` links from a single
    markdown document that is rendered using our own renderer.
    """

    def __init__(self, md_file):
        """ Open a Markdown document and find all links in `<a href .../>`.
        """
        # Store important information about this document.
        self.md_file = md_file
        self.md_dir = os.path.dirname(md_file)

        # Read in Markdown and generate HTML with our parser.
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown_raw_data = f.read()
        md = markdown.Markdown(extensions=mdextensions)
        md.page_root = self.md_dir
        html = md.convert(markdown_raw_data)

        # Interpret with the BeautifulSoup HTML scraping library.
        soup = BeautifulSoup(html, 'html.parser')

        tags_to_search = {
            'img': 'src',
            'a': 'href',
            'video': 'src',
            'table': 'source',
            'embed': 'src',
        }

        self.references = set()
        for k, v in tags_to_search.items():
            links = soup.find_all(k)

            for link in links:
                if link.get('href'):
                    if link.get('href').find('http:') > -1 or link.get('href').find('https:') > -1:
                        val = link.get(v)
                        if val:
                            self.references.add(val)
                else:
                    val = link.get(v)
                    if val:
                        self.references.add(val)

    @property
    def web_links(self):
        """ Generate a list of web links from our cached links.
        """
        return [link for link in self.references if is_absolute(link)]

    @property
    def relative_links(self):
        """ Generate a list of relative file system links from our cached links.
        This converts from a web path to a path on disk then normalises the path to the current directory.
        """
        def _norm(path):
            return os.path.join(self.md_dir, urllib.request.url2pathname(path))

        return [_norm(link) for link in self.references if not is_absolute(link)]

    @staticmethod
    def validate_url(address):
        """ Returns `True` if page at address returns with status code 200 (ok) otherwise returns `False`.
        """
        try:
            request = requests.head(address)
            return request.status_code, address

        except requests.exceptions.RequestException:
            return False, address

    def detect_broken_links(self, process_pool):
        """ Go through all the `web_links` and the `relative_links` and report
        which are broken (i.e. do not resolve to HTTP200OK or a file on disk).
        """
        result = process_pool.map(self.validate_url, self.web_links)
        for response, url in result:
            if not response == 200:
                yield url + ' Status: ' + (responses[response] if response is int else "Exception")

        for file in self.relative_links:
            if not os.path.exists(file):
                yield file


def generate_metadata(path):
    """ Add relevant metadata to the top of the markdown file at the passed path.
    Title is drawn from the filename, Date from the last modified timestamp, Version defaults at 1.0.0,
    Nav is generated from the filepath, and Authors are generated from the git contributors (if applicable) and
    are otherwise left blank.

    Warning: Does not check if there is existing metadata.
    """
    s = subprocess.getoutput(f"git log -p {path}")
    lines = s.split(os.linesep)
    authors = set([re.search(r'<(.*)>', line).group(1)for line in lines if 'Author:' in line])

    file_status = os.stat(path)

    nav_path = os.path.sep.join(path.split(os.path.sep)[1:])
    metadata = {
        'title': ' '.join(
            path
            .split('.')[0]
            .split(os.path.sep)[-1]
            .replace('_', ' ')
            .replace('-', ' ')
            .title()
            .split()
        ),
        'desc': '',
        'date': datetime.datetime.utcfromtimestamp(file_status.st_mtime).strftime('%Y/%m/%d'),
        'version': '1.0.0',
        'template': '',
        'nav': nav_path.replace(os.path.sep, '>').title().split('.')[0],
        'percent': '100',
        'authors': ' '.join(authors),
    }

    result = ""
    for key in metadata.keys():
        result += ('{}:{}{}\n'.format(key, '\t' if len(key) > 6 else '\t\t', metadata[key]))

    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(result)
        f.write(content)


class ReloadHandler(PatternMatchingEventHandler):
    """ Rebuild the document metadata / navigation cache when markdown files are updated
    in the documents directory. """
    def __init__(self, app):
        super(ReloadHandler, self).__init__(patterns=['*.md'], ignore_directories=False, case_sensitive=False)
        self.flask_app = app

    def on_any_event(self, event):
        self.flask_app.build_navigation_cache()


global CMD_ARGS, NAV_MENU, PROJECT_LOGO, WKHTMLTOPDF_BINARY, PDF_GENERATION_ENABLED, PORT_NUMBER

CMD_ARGS = None
NAV_MENU = {}
PROJECT_LOGO = None
WKHTMLTOPDF_BINARY = None
PDF_GENERATION_ENABLED = False


def main():
    """ Application entrypoint. """
    global PORT_NUMBER
    PORT_NUMBER = 5000

    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description='docnado: Lightweight tool for rendering \
                                     Markdown documentation with different templates.')

    parser.add_argument('--html', action='store', dest='html_output_dir',
                        help='Generate a static site from the server and output to the \
                        specified directory.')

    parser.add_argument('--pdf', action='store', dest='pdf_output_dir',
                        help='Generate static PDFs from the server and output to the \
                        specified directory.')

    parser.add_argument('--nav-limit', action='store', dest='nav_limit',
                        default=None,
                        help='Include certain document trees only based on a comma separated \
                        list of nav strings. e.g. Tooling,Document')

    parser.add_argument('--new', action="store_true", dest='new_project',
                        default=False,
                        help='Copy the `docs` and `styles` folder into the working directory \
                        and output a config file that addresses them. Does not overwrite existing files.')

    parser.add_argument('--new-force', action="store_true", dest='new_project_force',
                        default=False,
                        help='Copy the `docs` and `styles` folder into the working directory \
                        and output a config file that addresses them. Force deletion of existing files.')

    parser.add_argument('--dirs', action="store_true", dest='show_dirs',
                        default=False,
                        help='Display the different directories the software is using \
                        to search for documentation and styles.')

    parser.add_argument('--generate-meta', action="store", dest='generate_meta',
                        default=False,
                        help='Generate metadata for markdown files in the specified directory.')

    parser.add_argument('--find-orphans', action="store_true", dest='find_orphans',
                        default=False,
                        help='Identify unused media assets (orphans)')

    parser.add_argument('--find-broken-links', action="store_true", dest='find_broken_links',
                        default=False,
                        help='Identify broken external links.')

    parser.add_argument('--port', action="store", dest='new_port_number',
                        default=False,
                        help='Specify a port for the docnado server')

    parser.add_argument('--host', action="store", dest='set_host',
                        default=False,
                        help='Set the docnado development server to listen on IP addresses.')

    # Import the command line args and make them application global.
    global CMD_ARGS
    args = parser.parse_args()
    CMD_ARGS = args

    # Load config from the environment and validate it.
    global PROJECT_LOGO, PDF_GENERATION_ENABLED, NAV_MENU, WKHTMLTOPDF_BINARY
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    flask_debug = os.environ.get('DN_FLASK_DEBUG', FALSE) == TRUE
    watch_changes = os.environ.get('DN_RELOAD_ON_CHANGES', TRUE) == TRUE

    WKHTMLTOPDF_BINARY = ('wkhtmltopdf_0.12.5.exe' if platform.system() == 'Windows' else 'wkhtmltopdf')
    PDF_GENERATION_ENABLED = check_pdf_generation_cap()

    dir_documents = os.environ.get('DN_DOCS_DIR', os.path.join(os.getcwd(), 'docs'))
    dir_style = os.environ.get('DN_STYLE_DIR', os.path.join(os.getcwd(), 'style'))
    logo_location = os.environ.get('DN_PROJECT_LOGO', os.path.join(os.getcwd(), 'logo.png'))

    # If `style` folder does not exist, use the one in site-packages.
    if not os.path.exists(dir_style) and not os.path.isdir(dir_style):
        dir_style = os.path.join(os.path.dirname(__file__), 'style')

    # Attempt to load the project logo into a base64 data uri.
    PROJECT_LOGO = load_project_logo(logo_location)

    # Compute the static and template directories.
    dir_static = os.path.join(dir_style, 'static')
    dir_templates = os.path.join(dir_style, 'templates')

    # If the user is asking to create a new project.
    if args.new_project:
        copy_local_project()
        sys.exit()

    if args.new_project_force:
        copy_local_project(force=True)
        return 0

    if args.new_port_number:
        PORT_NUMBER = int(args.new_port_number)

    if args.generate_meta:
        doc_files = glob.iglob(args.generate_meta + '/**/*.md', recursive=True)
        for i in doc_files:
            generate_metadata(i)
        return 0

    if args.find_orphans:
        # Find all the assets in the directory/subdirectories recursively and append their file path to a list.
        files = glob.glob((dir_documents + '/**/*.*'), recursive=True)
        files = [f for f in files if not os.path.isdir(f)]
        orphans = find_orphans(files)
        if orphans:
            print(f'{len(orphans)} Unused assets (orphans):\n\t' + '\n\t'.join(orphans))
            return -1

        return 0

    if args.find_broken_links:
        process_pool = Pool(processes=10)
        md_files = glob.glob((dir_documents + '/**/*.md'), recursive=True)
        md_reports = tuple((md, list(DocumentLinks(md).detect_broken_links(process_pool))) for md in md_files)
        num_broken = 0
        for file, report in md_reports:
            if report:
                num_broken += len(report)
                print(f'{file}\n\t' + '\n\t'.join(report))
        return -1 if num_broken else 0

    if args.show_dirs:
        print('The following directories are being used: ')
        print('\t', f'Documents  -> {dir_documents}')
        print('\t', f'Logo       -> {logo_location}')
        print('\t', f'Style      -> {dir_style}')
        print('\t', f' Static    -> {dir_static}')
        print('\t', f' Templates -> {dir_templates}')
        sys.exit()

    if not os.path.exists(dir_documents) and not os.path.isdir(dir_documents):
        print(f'Error: Documents directory "{dir_documents}" does not exist.  \
        Create one called `docs` and fill it with your documentation.', file=sys.stderr)
        sys.exit(-1)

    if not os.path.exists(dir_static) and not os.path.isdir(dir_static):
        print(f'Error: Static directory "{dir_static}" does not exist.', file=sys.stderr)
        sys.exit(-1)

    if not os.path.exists(dir_templates) and not os.path.isdir(dir_templates):
        print(f'Error: Templates directory "{dir_templates}" does not exist.', file=sys.stderr)
        sys.exit(-1)

    # Create the server.
    app = Flask(__name__,
                static_url_path='',
                template_folder=dir_templates,
                static_folder=dir_static)

    # Attach routes and filters.
    configure_flask(app, dir_documents)

    # Output PDF files.
    if args.pdf_output_dir:
        if not check_pdf_generation_cap():
            print(f'Error: PDF generation requires WkHTMLtoPDF.', file=sys.stderr)
            sys.exit(-1)

        def gen_pdfs():
            time.sleep(2)
            generate_static_pdf(
                app, dir_documents, os.path.join(os.getcwd(), args.pdf_output_dir)
            )
            time.sleep(5)
            os.kill(os.getpid(), signal.SIGTERM)

        t1 = threading.Thread(target=gen_pdfs)
        t1.start()
        app.run(debug=flask_debug, threaded=True, port=PORT_NUMBER)
        sys.exit()

    # Output a static site.
    if args.html_output_dir:
        PDF_GENERATION_ENABLED = False
        try:
            generate_static_html(app, dir_documents, os.path.join(os.getcwd(), args.html_output_dir))
            index_html = """ <!DOCTYPE html>
                <html>
                    <head>
                        <meta http-equiv="refresh" content="0; url=./w/">
                    </head>
                <body>
                </body>
                </html>"""
            with open(os.path.join(os.getcwd(), args.html_output_dir, 'index.html'), 'w') as f:
                f.write(index_html)
        except Exception:
            traceback.print_exc(file=sys.stderr)
            sys.exit(-1)
        sys.exit()

    # Watch for any changes in the docs or style directories.
    dn_watch_files = []
    observer = None
    if watch_changes:
        observer = Observer()
        observer.schedule(ReloadHandler(app), path=dir_documents, recursive=True)
        observer.start()
        dn_watch_files = build_reload_files_list([__name__, dir_style])

    # Run the server.
    if args.set_host:
        try:
            print('Attempting set sevelopment server listen on public IP address: ' + args.set_host)
            print('WARNING: The Docnado development environment is intended to be used as a development tool ONLY, '
                  'and is not recommended for use in a production environment.')
            app.run(debug=flask_debug, port=PORT_NUMBER, extra_files=dn_watch_files, host=args.set_host)
        except OSError as e:
            print(e)
            print(f'Error initialising server.')
        except KeyboardInterrupt:
            pass
        finally:
            if observer:
                observer.stop()
                observer.join()
    else:
        try:
            app.run(debug=flask_debug, port=PORT_NUMBER, extra_files=dn_watch_files)
        except OSError as e:
            print(e)
            print(f'Error initialising server.')
        except KeyboardInterrupt:
            pass
        finally:
            if observer:
                observer.stop()
                observer.join()


# if running brainerd directly, boot the app
if __name__ == "__main__":
    main()
