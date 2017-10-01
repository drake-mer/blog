---
layout: post
title:  "Running a Jekyll Blog on Debian 9"
date:   2017-07-23 14:20:34 +0200
categories: jekyll update debian static blogging
published: false
---

I started by sailing through a sea of documentation to automate the deployment
of a [Zinnia Blog][zinnia-django-blog] on a remote debian VPS.

I quickly noticed that it wouldn't get me anywhere something usable, so I decided to
deploy a static blog based on simple git-hooks for automatic publication and
using [Jekyll][jekyll-gh].

Why Jekyll ?
- It is a widely used static website generator, with a huge community.
- It seems really easy to use and to tweak.
- The primary language is markdown
- To use it could allow me to practice some Ruby skills

There is other static blog generator around, coded with many languages, but
Jekyll is at the moment the easiest to start with and to integrate with my workflow.

I am not, at the moment, really familiar with the ruby environment,
but running `gem install jekyll` so far has not given me any problem. Some dependencies
had to be installed on debian to be able to build the blog engine, but I limited the import
debian packages to a strict minimum by installing everything with `gem` in my user folder.

The little I saw about `Gemfile`s, this way of packaging dependencies is quite equivalent
to the `requirements.txt`
python file, but the Ruby ecosystem seems a little bit neater and sophisticated.

Hopefully also, there is not a ton of build systems for Ruby as there is in python,
even if [pip][pip] is now the preferred way to manage the
dependencies of a project as far I can tell.

To install the gem locally, you can follow the indications
described on the [archlinux wiki][wiki-gem-archlinux].

The [deployment section][jekyll-docs-deployment]
gives a git post-receive hook to build
your website after each push on the git remote repository. I had to
put an additional file at the top of this shell script to put the
user-wide installation of jekyll in the path.

{% highlight bash %}
PATH="$(ruby -e 'print Gem.user_dir')"  # to get the Gem install file into the path
{% endhighlight %}

To be able to serve the blog, I added a really simple nginx configuration
that does the job easily.

{% highlight nginx %}
  server {
    location / {
     root /var/www/jekyll-blog;
    }
    server_name david-kremer.fr;
    access_log /var/log/nginx/jekyll-blog.log;
}
{% endhighlight %}

In the end, it was more rewarding to achieve this than trying the hard way to publish
a dynamic blog based on django.

The task of running a django blog on a distant VPS implies to
run a database engine, manage automatic deployment if you want to hack the blog
engine (that I plan to do), monitoring the WSGI job, doing the database backup and maintenance, etc.

What I will do next ? I plan to use the jekyll platform as a publishing tool, but I have
specific use cases in mind, so I will probably set myself on the track to code
jekyll plugins. First of all, I want to tweak a little bit my configuration, because
the current view is not really beautiful in my opinion. I will have to learn a little bit of
Ruby as well to get the job done.

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-docs-deployment]: https://jekyllrb.com/docs/deployment-methods/
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
[zinnia-django-blog]: https://github.com/Fantomas42/django-blog-zinnia
[wiki-gem-archlinux]: https://wiki.archlinux.org/index.php/ruby
[pip]: https://pypi.python.org/pypi/pip
