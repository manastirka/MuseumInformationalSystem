#!/usr/bin/env python3
"""
Generate HTML report from JSON test results.
Usage: python generate_html_report.py test_report.json
"""

import json
import sys
import os
from datetime import datetime
from string import Template

# Using Template with $var syntax to avoid CSS brace conflicts
HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Museum System - Test Report</title>
    <style>
        :root {
            --pass-color: #28a745;
            --fail-color: #dc3545;
            --error-color: #6f42c1;
            --skip-color: #ffc107;
            --bg-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #212529;
            --border-color: #dee2e6;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            padding: 20px;
        }

        .container { max-width: 1400px; margin: 0 auto; }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        header h1 { font-size: 2rem; margin-bottom: 5px; }
        header .subtitle { opacity: 0.9; font-size: 0.95rem; }

        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            border-left: 4px solid var(--border-color);
        }

        .card.pass { border-left-color: var(--pass-color); }
        .card.fail { border-left-color: var(--fail-color); }
        .card.error { border-left-color: var(--error-color); }
        .card.skip { border-left-color: var(--skip-color); }
        .card.total { border-left-color: #17a2b8; }

        .card .number { font-size: 2.5rem; font-weight: bold; line-height: 1; }
        .card.pass .number { color: var(--pass-color); }
        .card.fail .number { color: var(--fail-color); }
        .card.error .number { color: var(--error-color); }
        .card.skip .number { color: var(--skip-color); }
        .card.total .number { color: #17a2b8; }
        .card .label { font-size: 0.9rem; color: #6c757d; margin-top: 5px; }

        .progress-bar {
            height: 30px;
            background: var(--border-color);
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
            display: flex;
        }

        .progress-segment {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.85rem;
            font-weight: bold;
        }

        .progress-segment.pass { background: var(--pass-color); }
        .progress-segment.fail { background: var(--fail-color); }
        .progress-segment.error { background: var(--error-color); }
        .progress-segment.skip { background: var(--skip-color); }

        .section {
            background: var(--card-bg);
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }

        .section-header {
            background: #e9ecef;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 1.1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-header:hover { background: #dee2e6; }
        .section-header .badge { display: inline-flex; align-items: center; gap: 8px; }
        .section-header .count {
            background: #6c757d;
            color: white;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 0.85rem;
        }

        .section-content { padding: 0; max-height: 0; overflow: hidden; transition: max-height 0.3s; }
        .section-content.expanded { max-height: none; }

        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid var(--border-color); }
        th { background: #f8f9fa; font-weight: 600; font-size: 0.9rem; color: #495057; }
        tr:hover { background: #f8f9fa; }

        .status-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-badge.pass { background: #d4edda; color: #155724; }
        .status-badge.fail { background: #f8d7da; color: #721c24; }
        .status-badge.error { background: #e2d5f0; color: #4a1c7c; }
        .status-badge.skip { background: #fff3cd; color: #856404; }

        .message { font-size: 0.85rem; color: #6c757d; max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .failures-section { border-left: 4px solid var(--fail-color); }
        .failures-section .section-header { background: #f8d7da; }
        .duration { font-size: 0.85rem; color: #6c757d; }

        footer { text-align: center; padding: 20px; color: #6c757d; font-size: 0.9rem; }

        .filter-bar { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid var(--border-color);
            background: white;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .filter-btn:hover, .filter-btn.active { background: #667eea; border-color: #667eea; color: white; }

        @media (max-width: 768px) {
            .summary-cards { grid-template-columns: repeat(2, 1fr); }
            th, td { padding: 8px 10px; font-size: 0.9rem; }
            .message { max-width: 150px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏛️ Museum System Test Report</h1>
            <div class="subtitle">Generated: $timestamp | Duration: ${duration}s</div>
        </header>

        <div class="summary-cards">
            <div class="card total"><div class="number">$total</div><div class="label">Total Tests</div></div>
            <div class="card pass"><div class="number">$passed</div><div class="label">Passed</div></div>
            <div class="card fail"><div class="number">$failed</div><div class="label">Failed</div></div>
            <div class="card error"><div class="number">$errors</div><div class="label">Errors</div></div>
            <div class="card skip"><div class="number">$skipped</div><div class="label">Skipped</div></div>
        </div>

        <div class="progress-bar">
            <div class="progress-segment pass" style="width: ${pass_pct}%">${pass_pct}%</div>
            <div class="progress-segment fail" style="width: ${fail_pct}%">${fail_pct}%</div>
            <div class="progress-segment error" style="width: ${error_pct}%">${error_pct}%</div>
            <div class="progress-segment skip" style="width: ${skip_pct}%">${skip_pct}%</div>
        </div>

        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterResults('all')">All</button>
            <button class="filter-btn" onclick="filterResults('PASS')">Passed</button>
            <button class="filter-btn" onclick="filterResults('FAIL')">Failed</button>
            <button class="filter-btn" onclick="filterResults('ERROR')">Errors</button>
            <button class="filter-btn" onclick="filterResults('SKIP')">Skipped</button>
        </div>

        $failures_section

        $category_sections

        <footer>
            Museum Information System - Automated Test Report<br>
            Pass Rate: $pass_rate
        </footer>
    </div>

    <script>
        document.querySelectorAll('.section-header').forEach(header => {
            header.addEventListener('click', () => {
                const content = header.nextElementSibling;
                content.classList.toggle('expanded');
                const arrow = header.querySelector('.arrow');
                if (arrow) arrow.textContent = content.classList.contains('expanded') ? '▼' : '▶';
            });
        });

        function filterResults(status) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.toLowerCase().includes(status.toLowerCase()) || (status === 'all' && btn.textContent === 'All')) {
                    btn.classList.add('active');
                }
            });
            document.querySelectorAll('table tr[data-status]').forEach(row => {
                row.style.display = (status === 'all' || row.dataset.status === status) ? '' : 'none';
            });
        }

        const failuresContent = document.querySelector('.failures-section .section-content');
        if (failuresContent) failuresContent.classList.add('expanded');
    </script>
</body>
</html>
""")

def generate_html_report(json_file, output_file=None):
    """Generate HTML report from JSON test results."""

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    summary = data.get('summary', {})
    by_category = data.get('by_category', {})
    failures = data.get('failures', [])

    total = summary.get('total', 0)
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    errors = summary.get('errors', 0)
    skipped = summary.get('skipped', 0)

    pass_pct = round(passed / total * 100, 1) if total > 0 else 0
    fail_pct = round(failed / total * 100, 1) if total > 0 else 0
    error_pct = round(errors / total * 100, 1) if total > 0 else 0
    skip_pct = round(skipped / total * 100, 1) if total > 0 else 0

    # Generate failures section
    failures_section = ""
    if failures:
        failures_html = ""
        for r in failures:
            status_class = r['status'].lower()
            msg = (r.get('message', '') or '').replace('"', '&quot;')
            failures_html += f"""
            <tr data-status="{r['status']}">
                <td><span class="status-badge {status_class}">{r['status']}</span></td>
                <td>{r['category']}</td>
                <td>{r['name']}</td>
                <td class="message" title="{msg}">{msg}</td>
            </tr>"""

        failures_section = f"""
        <div class="section failures-section">
            <div class="section-header">
                <span class="badge"><span class="arrow">▼</span> ⚠️ Failures & Errors</span>
                <span class="count">{len(failures)}</span>
            </div>
            <div class="section-content expanded">
                <table>
                    <thead><tr><th style="width:100px">Status</th><th style="width:150px">Category</th><th>Test Name</th><th>Message</th></tr></thead>
                    <tbody>{failures_html}</tbody>
                </table>
            </div>
        </div>"""

    # Generate category sections
    category_sections = ""
    for category, results in sorted(by_category.items()):
        results_html = ""
        for r in results:
            status_class = r['status'].lower()
            duration = f"{r.get('duration', 0):.2f}s" if r.get('duration') else "-"
            msg = (r.get('message', '') or '').replace('"', '&quot;')
            results_html += f"""
            <tr data-status="{r['status']}">
                <td><span class="status-badge {status_class}">{r['status']}</span></td>
                <td>{r['name']}</td>
                <td class="message" title="{msg}">{msg}</td>
                <td class="duration">{duration}</td>
            </tr>"""

        cat_pass = sum(1 for r in results if r['status'] == 'PASS')
        cat_fail = sum(1 for r in results if r['status'] == 'FAIL')
        cat_err = sum(1 for r in results if r['status'] == 'ERROR')

        if cat_fail > 0 or cat_err > 0:
            status_indicator = "❌"
        elif cat_pass == len(results):
            status_indicator = "✅"
        else:
            status_indicator = "⚠️"

        category_sections += f"""
        <div class="section">
            <div class="section-header">
                <span class="badge"><span class="arrow">▶</span> {status_indicator} {category}</span>
                <span class="count">{len(results)} tests</span>
            </div>
            <div class="section-content">
                <table>
                    <thead><tr><th style="width:100px">Status</th><th>Test Name</th><th>Message</th><th style="width:80px">Duration</th></tr></thead>
                    <tbody>{results_html}</tbody>
                </table>
            </div>
        </div>"""

    # Generate final HTML
    html = HTML_TEMPLATE.substitute(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        duration=round(summary.get('duration_seconds', 0), 1),
        total=total,
        passed=passed,
        failed=failed,
        errors=errors,
        skipped=skipped,
        pass_pct=pass_pct,
        fail_pct=fail_pct,
        error_pct=error_pct,
        skip_pct=skip_pct,
        pass_rate=summary.get('pass_rate', '0%'),
        failures_section=failures_section,
        category_sections=category_sections
    )

    if output_file is None:
        output_file = json_file.replace('.json', '.html')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML report generated: {output_file}")
    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python generate_html_report.py <test_report.json> [output.html]")
        sys.exit(1)

    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(json_file):
        print(f"Error: File not found: {json_file}")
        sys.exit(1)

    generate_html_report(json_file, output_file)
