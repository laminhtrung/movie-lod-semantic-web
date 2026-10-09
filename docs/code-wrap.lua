local esc = {['_']='\\_', ['%']='\\%', ['#']='\\#', ['&']='\\&', ['$']='\\$', ['{']='\\{', ['}']='\\}', ['\\']='\\textbackslash{}', ['^']='\\textasciicircum{}', ['~']='\\textasciitilde{}'}
local function wrap_token(value)
  local parts = {}
  local index = 0
  for _, c in utf8.codes(value) do
    local char = utf8.char(c)
    index = index + 1
    if index > 1 and char:match('[A-Z]') then table.insert(parts, '\\allowbreak{}') end
    table.insert(parts, esc[char] or char)
    if char:match('[/_.:%-]') or index % 8 == 0 then table.insert(parts, '\\allowbreak{}') end
  end
  return table.concat(parts)
end
function Code(el)
  if FORMAT ~= 'latex' then return nil end
  return pandoc.RawInline('latex', '\\texttt{'..wrap_token(el.text)..'}')
end
function Str(el)
  if FORMAT == 'latex' and #el.text > 12 and el.text:match('^[A-Za-z0-9_./:%-,;()]+$') then
    return pandoc.RawInline('latex', wrap_token(el.text))
  end
end
