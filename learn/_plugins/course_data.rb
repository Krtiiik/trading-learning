# Reads facts that live outside learn/ into site.data, so the site never keeps a copy:
# - site.data.glossary: the **Term**: definition entries of ../.claude/CONTEXT.md
#   (sent to Claude with every Ask Claude request, as part of the course brief)
# - site.data.mission_text: MISSION.md without its front matter (also part of the course brief)
# - site.data.universe_size: how many symbols ../universe.toml lists (dashboard facts row)
module CourseData
  class Generator < Jekyll::Generator
    safe true
    priority :highest

    def generate(site)
      repo = File.expand_path("..", site.source)
      site.data["glossary"] = glossary(File.join(repo, ".claude", "CONTEXT.md"))
      site.data["universe_size"] = universe_size(File.join(repo, "universe.toml"))
      site.data["mission_text"] = without_front_matter(File.join(site.source, "MISSION.md"))
    end

    private

    def glossary(path)
      return [] unless File.exist?(path)

      File.read(path, encoding: "utf-8").scan(/^\*\*(.+?)\*\*:\s*(.+)$/).map do |term, definition|
        { "term" => term, "definition" => definition.strip }
      end
    end

    def without_front_matter(path)
      return "" unless File.exist?(path)

      File.read(path, encoding: "utf-8").sub(/\A---\s*\n.*?\n---\s*\n/m, "").strip
    end

    def universe_size(path)
      return nil unless File.exist?(path)

      text = File.read(path, encoding: "utf-8")
      list = text[/symbols\s*=\s*\[(.*?)\]/m, 1]
      list && list.lines.map { |l| l.sub(/#.*/, "") }.join.scan(/"[^"]+"/).size
    end
  end
end
