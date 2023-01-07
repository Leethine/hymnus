#!/usr/bin/python3
import sys, os, shutil, re

sys.path.append('../')
from html_creator import HtmlCreator

class AboutHtmlCreator(HtmlCreator):
  def __init__(self) -> None:
    super().__init__()
  
  def create_intro_section(self, intro_text: str) -> str:
    return "<p class=\"lead\">" + intro_text + "</p>"

  def create_feature_section(self, textbody: str, bulletlist: list) -> str:
    html_section_str = "<p class=\"lead\">" + textbody + "</p>\n"
    if not bulletlist:
      pass
    else:
      html_section_str += "<ul>\n"
      for item in bulletlist:
        html_section_str += "<li>" + str(item) + "</li>\n"
      html_section_str += "<ul>\n"

    return html_section_str

  def create_about_html_file(self, intro_text: str, feature_text: str, feature_list: list) -> str:
    # handle intro text
    self.reset_tag("<!--ABOUTINTROTEXTRFBEGIN-->", "<!--ABOUTINTROTEXTRFEND-->")
    self.read_template_file()
    self.replace_html_section(self.create_intro_section(intro_text))
    
    # handle feature text and list
    self.reset_tag("<!--ABOUTFEATURETEXTRFBEGIN-->", "<!--ABOUTFEATURETEXTRFEND-->")
    self.replace_html_section(self.create_feature_section(feature_text, feature_list))

    # write html file
    return self.write_index_file()

if __name__ == "__main__":
  intro = """
  Hymnus (Hypertext Management for Musical Notation Scripts)<br>
  is a html-based gui for musical notation source-code library
  management.
  """
  feature = ""
  bullets = ["One", "Two", "Three"]

  ahc = AboutHtmlCreator()
  ahc.create_about_html_file(intro, feature, bullets)
