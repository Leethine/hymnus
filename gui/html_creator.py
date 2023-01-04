#!/usr/bin/python3
import sys, os, shutil, re

class HtmlCreator:
  def __init__(self) -> None:
    self.HTML_TEMPLATE = "template"
    self.HTML_INDEX = "index"
    self.HTML_EXTENSION = ".html"
    self.HTML_TEMPLATE_FILE = self.HTML_TEMPLATE + self.HTML_EXTENSION
    self.HTML_INDEX_FILE = self.HTML_INDEX + self.HTML_EXTENSION
    
    self.REPLACE_TAG_BEGIN = "<!--#TOBESET-->"
    self.REPLACE_TAG_END = "<!--#TOBESET-->"

    self.HTMLFILE_BUFFER = ""

  def reset_tag(self, tag_begin: str, tag_end: str) -> None:
    self.REPLACE_TAG_BEGIN = tag_begin
    self.REPLACE_TAG_END = tag_end
  
  def replace_html_section(self, section_str: str) -> str:
    """
    Write the html section between replace tags.
    The tags are defined by member self.REPLACE_TAG_BEGIN and END
    """
    # find pos span of the replaceable field
    posStart = re.search(re.escape(self.REPLACE_TAG_BEGIN), self.HTMLFILE_BUFFER).start()
    posEnd = re.search(re.escape(self.REPLACE_TAG_END), self.HTMLFILE_BUFFER).end()
    # concatenate new file str by replacing the field in between
    self.HTMLFILE_BUFFER = self.HTMLFILE_BUFFER[:posStart] \
                + section_str \
                + self.HTMLFILE_BUFFER[posEnd:]
    
    return self.HTMLFILE_BUFFER
  
  def read_template_file(self) -> str:
    """
    Read html template file into buffer.
    """
    assert(os.path.exists(self.HTML_TEMPLATE_FILE))

    with open(self.HTML_TEMPLATE_FILE, "r") as htmlfile:
      self.HTMLFILE_BUFFER = "".join(htmlfile.readlines())
    
    # prepare the new html file while reading the template file
    return self.HTMLFILE_BUFFER
  
  def write_index_file(self) -> str:
    """
    Write from buffer to new index(*).html file
    """
    with open(self.HTML_INDEX_FILE, "w") as htmlfile:
      htmlfile.write(self.HTMLFILE_BUFFER)
    
    return self.HTMLFILE_BUFFER
  