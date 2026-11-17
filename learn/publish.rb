# Prepares the built site for publishing as one multi-file Claude artifact.
# Run from learn/ after `bundle exec jekyll build`:  ruby publish.rb
#
# The artifact host wraps the main page in its own document skeleton, so the dashboard
# (_site/index.html) is rewritten without its doctype/html/head/body tags into
# _publish/index.html. Every other built file is published as is, listed in
# _publish/files.json as {published path: source path relative to _site/}.
require "fileutils"
require "json"

site = File.expand_path("_site", __dir__)
out = File.expand_path("_publish", __dir__)
abort "No _site/ yet: run `bundle exec jekyll build` first." unless File.exist?(File.join(site, "index.html"))

FileUtils.mkdir_p(out)
page = File.read(File.join(site, "index.html"), encoding: "utf-8")
page = page
  .sub(/\A\s*<!doctype html>\s*/i, "")
  .gsub(%r{</?html[^>]*>|</?head>|</?body[^>]*>}i, "")
  .sub(/<meta charset="utf-8">\s*/i, "")                       # the host's skeleton has these two
  .sub(/<meta name="viewport"[^>]*>\s*/i, "")
File.write(File.join(out, "index.html"), page.strip + "\n")

files = Dir.glob("**/*", base: site).sort
  .reject { |path| File.directory?(File.join(site, path)) || path == "index.html" }
  .to_h { |path| [path, path] }
File.write(File.join(out, "files.json"), JSON.pretty_generate(files) + "\n")

puts "Main page: #{File.join(out, 'index.html')}"
puts "#{files.size} other files (root: _site/): #{files.keys.join(', ')}"
