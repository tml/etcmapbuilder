# -*- coding: utf-8 -*-

"""
etcmapbuilder
~~~~~
This is a simple tool meant to help you create /etc/map rules for an AEM/Sling CMS.
"""
import sys
import os
import errno
import six

try:
    from clint.textui import puts, indent, colored, prompt, validators
except ImportError as ex:
    print(ex)
    print("Unable to import the 'clint' library; you may be able to fix this with `pip install clint`")
    sys.exit(1)

def mkdir_sane(dir):
    try:
        if (six.PY3):
            os.makedirs(dir, 0o755, True)
        else:
            os.makedirs(dir, 0o755)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else:
            raise ex

puts(colored.green("You will need the following pieces of information to proceed safely:"))
puts("FQDN")
puts("Content Root")
readyOptions = [
    {'selector': '0', 'prompt': 'No {will exit immediately}', 'return': False},
    {'selector': '1', 'prompt': 'Yes', 'return': True}
]
ready = prompt.options("Are you prepared?", readyOptions)
if (ready):
    puts(colored.red("OK. Enter '.' at any non-option prompt to exit without saving."))
    print("OK")
    fqdn = prompt.query("What is the FQDN? :")
    if (fqdn == '.'):
        sys.exit(0)


    proposedContentRoot = prompt.query("What is the content root for {} [e.g., /content/foo/en/]".format(fqdn))
    if (proposedContentRoot == '.'):
        sys.exit(0)

    contentRoot = '/'.join([y for y in filter(None, proposedContentRoot.split('/')) if y not in ['content','en']])

    etcRoot = prompt.query("In which directory should these rules be created?")
    if (etcRoot == '.'):
        sys.exit(0)


primaryXMLString = """
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0" xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:mixinTypes="[cq:ReplicationStatus]"
    jcr:primaryType="sling:Mapping"
    sling:internalRedirect="[/content/{0}/en/,/,/content/dam/{0}/,/dam/]"/>
""".format(contentRoot)

rootDomainXMLString = """
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0" xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:mixinTypes="[cq:ReplicationStatus]"
    jcr:primaryType="sling:Mapping"
    sling:internalRedirect="/content/{0}/en.html"
    sling:match="{1}/$"/>
""".format(contentRoot, fqdn)


fqdnPrimary = "{}/{}".format(etcRoot, fqdn)
fqdnBare = "{}/{}".format(etcRoot, fqdn.replace(".", "_"))

puts("""
    If you proceed, we will write this to {0}/.content.xml:
    {1}

    and this to {2}/.content.xml:
    {3}

    """.format(colored.red(fqdnPrimary), primaryXMLString, colored.red(fqdnBare), rootDomainXMLString))

createRules = prompt.options("Go ahead with creating entries in path {}?".format(etcRoot), readyOptions)
if (createRules):
    mkdir_sane(etcRoot)

    mkdir_sane(fqdnPrimary)
    f = open("{}/.content.xml".format(fqdnPrimary), "w+")
    f.write(primaryXMLString)

    mkdir_sane(fqdnBare)
    f = open("{}/.content.xml".format(fqdnBare), "w+")
    f.write(rootDomainXMLString)

__version__ = '0.1.5'
__build__ = 0x000105
__copyright__ = 'Copyright 2015 Axis41 and Joey Smith'
__docformat__ = 'restructuredtext'
__author__ = 'Joey Smith'
__email__ = 'jsmith@axis41.com'
