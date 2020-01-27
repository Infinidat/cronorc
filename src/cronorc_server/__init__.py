__import__("pkg_resources").declare_namespace(__name__)

from os import path, pardir

PROJECTROOT = path.abspath(path.join(path.dirname(__file__),  # cronorc_server
                                     pardir,  # src,
                                     pardir,  # root
                                     ))
