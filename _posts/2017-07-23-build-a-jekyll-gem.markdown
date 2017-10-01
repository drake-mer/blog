---
layout: post
title:  "Creating a Neat Jekyll Theme"
date:   2017-07-23 14:20:34 +0200
categories: jekyll update gem theme
published: false
---

The standard theme [minima][minima] is quite neat. Really
a beautiful CSS, nothing is in the way of the reader, perfect
as a standard default template. However, I wanted to tweak it
a little bit to have something a little bit more personal.

There is about three possibilities to modify the basic template:

### Modify the Basic Bundle directly
{% highlight bash %}
[david@localhost _posts]$ ls -l $(bundle show minima)
total 28
drwxr-xr-x 2 david david 4096 23 juil. 14:19 assets
drwxr-xr-x 2 david david 4096 23 juil. 14:19 _includes
drwxr-xr-x 2 david david 4096 23 juil. 14:19 _layouts
-rw-r--r-- 1 david david 1079 23 juil. 14:19 LICENSE.txt
-rw-r--r-- 1 david david 6345 23 juil. 14:19 README.md
drwxr-xr-x 3 david david 4096 23 juil. 14:19 _sass
{% endhighlight %}
### Copying the gem into the Site Directory
### Create a New Gem

- Solution 1 is not my taste and not really useful if you want to do remote deployment
- Solution 2 is okay for quick tweaking of the minima default theme.
- Solution 3 is better overall for reuse though a little bit more complicated

Let's go for the number 3 then. I will register on


[jekyll-themes]: https://jekyllrb.com/docs/themes/
[minima]: https://github.com/jekyll/minima
