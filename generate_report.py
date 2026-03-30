#!/usr/bin/env python3
from __future__ import annotations

import math
from dataclasses import dataclass


def domain_pct(scores: list[int], item_idxs_1based: list[int]) -> float:
    vals = [scores[i-1] for i in item_idxs_1based]
    obtained = sum(vals)
    minv = 1 * len(vals)
    maxv = 7 * len(vals)
    return (obtained - minv) / (maxv - minv) * 100.0


def mean(a: list[int], b: list[int]) -> list[float]:
    return [(x+y)/2 for x,y in zip(a,b)]


def fmt_pct(x: float) -> str:
    return f"{x:.0f}%"


def esc(s: str) -> str:
    return (s.replace('&','&amp;')
             .replace('<','&lt;')
             .replace('>','&gt;'))


ITEMS = [
  "1. Overall objective(s) of the guideline are specifically described",
  "2. Health question(s) covered are specifically described",
  "3. Population (patients/public) to whom the guideline is meant to apply is specifically described",
  "4. Guideline development group includes individuals from all relevant professional groups",
  "5. Views and preferences of the target population (patients/public) have been sought",
  "6. Target users of the guideline are clearly defined",
  "7. Systematic methods were used to search for evidence",
  "8. Criteria for selecting the evidence are clearly described",
  "9. Strengths and limitations of the body of evidence are clearly described",
  "10. Methods for formulating the recommendations are clearly described",
  "11. Health benefits, side effects, and risks were considered in formulating the recommendations",
  "12. There is an explicit link between the recommendations and the supporting evidence",
  "13. The guideline has been externally reviewed by experts prior to publication",
  "14. A procedure for updating the guideline is provided",
  "15. The recommendations are specific and unambiguous",
  "16. Different options for management of the condition are clearly presented",
  "17. Key recommendations are easily identifiable",
  "18. Facilitators and barriers to its application are described",
  "19. Advice/tools on how the recommendations can be put into practice are provided",
  "20. The potential resource implications of applying the recommendations have been considered",
  "21. Monitoring and/or auditing criteria are presented",
  "22. The views of the funding body have not influenced the content of the guideline",
  "23. Competing interests of guideline development group members have been recorded and addressed",
]

DOMAINS = [
  ("1. Scope and purpose", [1,2,3]),
  ("2. Stakeholder involvement", [4,5,6]),
  ("3. Rigour of development", [7,8,9,10,11,12,13,14]),
  ("4. Clarity of presentation", [15,16,17]),
  ("5. Applicability", [18,19,20,21]),
  ("6. Editorial independence", [22,23]),
]

@dataclass
class Doc:
    key: str
    title: str
    url: str|None
    scores_a: list[int]
    scores_b: list[int]
    evidence: dict[int, list[str]]  # item -> list of evidence strings


DOCS: list[Doc] = [
  Doc(
    key="Doc 1",
    title="Onkopedia guideline (DGHO et al.), Sept 2024 — HTML + PDF export",
    url="https://www.onkopedia.com/en/onkopedia/guidelines/paroxysmal-nocturnal-hemoglobinuria-pnh/@@guideline/html/index.html",
    scores_a=[6,5,6, 5,3,5, 2,1,2,2,4,3,1,1, 6,6,6, 3,2,2,1, 3,5],
    scores_b=[6,5,6, 5,2,5, 2,1,2,2,4,3,1,1, 6,6,6, 2,2,2,1, 3,4],
    evidence={
      1:["PDF p5: ‘Paroxysmal Nocturnal Hemoglobinuria (PNH) — Date of document: September 2024’ + summary framing."],
      3:["PDF p5: Summary describes disease + phenotypes; intended patient population implicitly PNH patients."],
      4:["PDF p5: Authors listed; multiple institutions/countries."],
      5:["PDF p34–35: patient/advocacy affiliations appear (e.g., ‘Aplastische Anämie & PNH e.V.’, ‘Stiftung lichterzellen’) → partial patient voice evidence."],
      7:["Not explicitly described in PDF: no systematic search strategy or databases/terms provided."],
      10:["Not explicitly described: recommendation formulation method not stated (no GRADE/consensus method described)."],
      15:["PDF ToC + structured Therapy section; multiple concrete statements (‘… is recommended…’)."],
      16:["PDF ToC: supportive, curative, drug therapy, special situations; multiple management options."],
      20:["Resource/cost implications not explicit (no cost/budget section identified)."],
      23:["PDF p35: ‘Disclosure of Potential Conflicts of Interest according to the rules of the responsible Medical Societies.’ (details not included in extract)."],
    }
  ),
  Doc(
    key="Doc 2",
    title="Consensus statement (Hematology, Transfusion and Cell Therapy) — PDF",
    url=None,
    scores_a=[5,4,5, 5,2,4, 2,1,2,3,5,3,1,1, 5,5,5, 4,3,4,2, 2,6],
    scores_b=[5,4,5, 4,2,4, 2,1,2,3,5,3,1,1, 5,5,5, 4,2,4,2, 2,6],
    evidence={
      1:["PDF p1–2: title ‘Consensus statement for diagnosis and treatment of PNH’ + introduction states purpose."],
      3:["PDF p1: clinical context is PNH patients; scope = diagnosis and treatment."],
      4:["PDF p1: multi-author, multi-center committee statement."],
      20:["PDF p7: ‘… main limitation … high cost … limited context of funding … public health system (SUS) … public budget…’"],
      23:["PDF p7: ‘Conflicts of interest: The authors declare no conflicts of interest.’"],
    }
  ),
  Doc(
    key="Doc 3",
    title="Systematic review + expert opinion (Adv Ther 2023) — PDF",
    url=None,
    scores_a=[4,4,4, 5,1,4, 6,5,5,5,4,5,2,2, 4,4,4, 2,1,1,1, 2,3],
    scores_b=[4,4,4, 5,1,4, 6,5,4,5,4,5,2,2, 4,4,4, 2,1,1,1, 2,3],
    evidence={
      7:["PDF p10: ‘Embase and PubMed/Medline systematic literature search … following the PRISMA method …’"],
      8:["PDF p10: inclusion filters ‘last 6 years’, full-text; search terms listed."],
      10:["PDF p10: ‘A modified Delphi method … consensus … ≥80% agreement…’"],
      5:["PDF p10: ‘As no patient was involved in the study…’"],
    }
  ),
]


def render_domain_table() -> str:
    rows=[]
    for name, idxs in DOMAINS:
        cells=[f"<td>{esc(name)}</td><td class=small>{esc(str(idxs).strip('[]'))}</td>"]
        for d in DOCS:
            pa=domain_pct(d.scores_a, idxs)
            pb=domain_pct(d.scores_b, idxs)
            pm=domain_pct([round(x) for x in mean(d.scores_a, d.scores_b)], idxs)
            cells.append(f"<td><div><b>{fmt_pct(pm)}</b></div><div class=small>A {fmt_pct(pa)} / B {fmt_pct(pb)}</div></td>")
        rows.append('<tr>'+''.join(cells)+'</tr>')
    return """
<table>
  <thead>
    <tr>
      <th>Domain</th>
      <th>Items</th>
      <th>Doc 1</th>
      <th>Doc 2</th>
      <th>Doc 3</th>
    </tr>
  </thead>
  <tbody>
  """ + "\n".join(rows) + """
  </tbody>
</table>
"""


def render_item_table() -> str:
    header = """
<table>
  <thead>
    <tr>
      <th style="width:34%">AGREE II item</th>
      <th style="width:22%">Doc 1 (A/B/Mean)</th>
      <th style="width:22%">Doc 2 (A/B/Mean)</th>
      <th style="width:22%">Doc 3 (A/B/Mean)</th>
    </tr>
  </thead>
  <tbody>
"""
    rows=[]
    for i, label in enumerate(ITEMS, start=1):
        row=[f"<td><b>{esc(label.split('.',1)[0])}</b> {esc(label.split('.',1)[1].strip())}</td>"]
        for d in DOCS:
            a=d.scores_a[i-1]
            b=d.scores_b[i-1]
            m=(a+b)/2
            ev = d.evidence.get(i, ["Not explicitly described / not found in extracted text."])
            ev_html = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in ev[:3]) + "</ul>"
            row.append(f"<td><div><b>{a}/{b}/{m:.1f}</b></div><div class=small>{ev_html}</div></td>")
        rows.append('<tr>'+''.join(row)+'</tr>')
    return header + "\n".join(rows) + "</tbody></table>"


def main() -> None:
    domain_html = render_domain_table()
    item_html = render_item_table()

    # Read template (existing report/index.html) and replace markers.
    import pathlib
    template = pathlib.Path('report/index.html').read_text(encoding='utf-8')

    def replace_between(s: str, start: str, end: str, new: str) -> str:
        i=s.find(start)
        j=s.find(end, i+len(start))
        if i==-1 or j==-1:
            raise SystemExit(f"marker not found: {start}..{end}")
        return s[:i+len(start)] + new + s[j:]

    # Insert into specific sections by simple string anchors.
    # Replace first TBD domain table and evidence section.
    template = template.replace('<!--DOMAIN_TABLE-->', domain_html)
    template = template.replace('<!--ITEM_TABLE-->', item_html)

    pathlib.Path('report/index.html').write_text(template, encoding='utf-8')
    pathlib.Path('docs/index.html').write_text(template, encoding='utf-8')


if __name__ == '__main__':
    main()
