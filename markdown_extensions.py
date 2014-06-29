# -*- coding: utf-8 -*-
import markdown
import re

from collections import OrderedDict

from django.template.loader import render_to_string
from django.template import Context

CITATION_RE = re.compile(r'\[@([;-@\w\s;]+)\]+')

from publications.models import Publication

class CitationExtension(markdown.Extension):
    safe_mode = False
    """ Citations plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md, md_globals):
        """ Insert ImagePreprocessor before ReferencePreprocessor. """
        md.preprocessors.add('dw-citations', CitationPreprocessor(md), '>html_block')

class CitationPreprocessor(markdown.preprocessors.Preprocessor):
    """django-wiki citation preprocessor - parse [@citekey] references. """

    def run(self, lines):
        footnotes = []

        # Find all matches in the current wiki page and create a unique list with preserved order
        new_lines = "\n".join(lines)
        matches = list(OrderedDict.fromkeys(CITATION_RE.findall(new_lines)))

        # Search the database for matching citations
        pubs = Publication.objects.filter(citekey__in=matches)
        present = pubs.values_list('citekey', flat=True)

        # Amend the matches to contain only those present in the database
        matches = [m for m in matches if m in present]

        # For each publication found, replace the citekey with the publication's format
        for pub in pubs:
            footnote  = matches.index(pub.citekey) + 1
            new_lines = new_lines.replace("[@%s]" % pub.citekey, "[^%d]" % footnote)

            # Mark footnote as safe
            footnotes.append("[^%d]: %s" % (
                footnote, self.markdown.htmlStash.store(pub.format_harvard(), safe=True)))

        return new_lines.split("\n") + footnotes

