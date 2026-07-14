function renderInlineMarkdown(text) {
  const parts = [];
  const linkRegex = /\[(.*?)\]\((https?:\/\/[^)]+)\)/g;
  let lastIndex = 0;
  let match;

  while ((match = linkRegex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }

    parts.push(
      <a key={`${match[2]}-${match.index}`} href={match[2]} target="_blank" rel="noreferrer" className="text-cyan-300 underline decoration-cyan-300/40 underline-offset-4">
        {match[1]}
      </a>
    );

    lastIndex = linkRegex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return parts.length > 0 ? parts : text;
}

function renderMarkdown(content) {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  const elements = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];

    if (line.startsWith("```")) {
      const language = line.slice(3).trim();
      const codeLines = [];
      index += 1;

      while (index < lines.length && !lines[index].startsWith("```")) {
        codeLines.push(lines[index]);
        index += 1;
      }

      elements.push(
        <pre key={`code-${index}`} className="overflow-x-auto rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-slate-100">
          {language ? <div className="mb-2 text-xs uppercase tracking-[0.2em] text-slate-500">{language}</div> : null}
          <code>{codeLines.join("\n")}</code>
        </pre>
      );
    } else if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];

      while (index < lines.length && /^\s*\d+\.\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*\d+\.\s+/, ""));
        index += 1;
      }

      elements.push(
        <ol key={`ol-${index}`} className="ml-5 list-decimal space-y-1 text-slate-200">
          {items.map((item, itemIndex) => <li key={itemIndex}>{renderInlineMarkdown(item)}</li>)}
        </ol>
      );
      continue;
    } else if (/^\s*[-*]\s+/.test(line)) {
      const items = [];

      while (index < lines.length && /^\s*[-*]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*[-*]\s+/, ""));
        index += 1;
      }

      elements.push(
        <ul key={`ul-${index}`} className="ml-5 list-disc space-y-1 text-slate-200">
          {items.map((item, itemIndex) => <li key={itemIndex}>{renderInlineMarkdown(item)}</li>)}
        </ul>
      );
      continue;
    } else if (/^\|.*\|$/.test(line) && index + 1 < lines.length && /-/.test(lines[index + 1])) {
      const tableRows = [line];
      index += 1;

      while (index < lines.length && /^\|.*\|$/.test(lines[index])) {
        tableRows.push(lines[index]);
        index += 1;
      }

      const headers = tableRows[0].split("|").filter(Boolean).map((cell) => cell.trim());
      const rows = tableRows.slice(2).map((row) => row.split("|").filter(Boolean).map((cell) => cell.trim()));

      elements.push(
        <div key={`table-${index}`} className="overflow-x-auto rounded-2xl border border-white/10 bg-white/5">
          <table className="min-w-full text-left text-sm text-slate-200">
            <thead className="bg-white/5 text-slate-100">
              <tr>{headers.map((header) => <th key={header} className="px-4 py-3 font-semibold">{header}</th>)}</tr>
            </thead>
            <tbody>
              {rows.map((row, rowIndex) => (
                <tr key={rowIndex} className="border-t border-white/10">
                  {row.map((cell, cellIndex) => <td key={cellIndex} className="px-4 py-3 align-top">{renderInlineMarkdown(cell)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      continue;
    } else if (line.trim()) {
      elements.push(<p key={`p-${index}`}>{renderInlineMarkdown(line)}</p>);
    }

    index += 1;
  }

  return elements;
}

export default function ChatMessage({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[85%] rounded-3xl px-4 py-3 shadow-lg ${isUser ? "bg-cyan-500 text-slate-950" : "border border-white/10 bg-white/5 text-slate-100"}`}>
        <div className="mb-2 text-xs font-semibold uppercase tracking-[0.25em] text-slate-400">
          {isUser ? "You" : "StudyAgent"}
        </div>
        <div className="space-y-3 text-sm leading-7">{renderMarkdown(content || "")}</div>
      </div>
    </div>
  );
}