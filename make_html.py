""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en-US"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  
  <link rel="shortcut icon" href="../../../images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="../../../style.css">
  <title>16-735 Module Materials</title>
  <script async="" src="analytics.js"></script><script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
    
    ga('create', 'UA-83215168-1', 'auto');
    ga('send', 'pageview');
  </script>
</head>
<body>
<h2>${header}</h2>
<p>
% for name,pretty in zip(names,pretty_names):
    <a href="${name}">${pretty}</a><br><br>
% endfor
</p>
</body>
</html>
"""

EXCLUDED = ['index.html','.DS_Store']

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    for meta_dir in os.listdir(args.directory):
        if not os.path.isdir(args.directory + meta_dir):
            continue
        print(args.directory + meta_dir + '/index.html')
        fnames = []
        for fname in sorted(os.listdir(args.directory + meta_dir)):
            if fname not in EXCLUDED:
                if os.path.isdir(args.directory + meta_dir + '/' + fname):
                    fnames.append(fname + '/index.html')
                else:
                    fnames.append(fname)
        pretty_names = [name.replace('_',' ').split('/index.html')[0] for name in fnames]
        print(fnames)
        header = (args.header if args.header else os.path.basename(args.directory + meta_dir))
        header =  'Module Materials: ' + header.replace('-',' ')
        with open(args.directory + meta_dir + '/index.html', 'w') as f:
            html = Template(INDEX_TEMPLATE).render(names=fnames, header=header, pretty_names=pretty_names)
            f.write(html)
        #print(Template(INDEX_TEMPLATE).render(names=fnames)), header=header))


if __name__ == '__main__':
    main()
