"""
Figure 1: Framework Overview — Criterion-Construction Framework (Skeleton + Skin + Readout States)
Figure 2: Layered Readout — L1 vs L2 decomposition of 452 direct-execution texts
Figure 3: ITSM Deployment Condition Modulation — BV rate × 5 models × 3 conditions
Figure 4: Cross-Scenario Comparison — tool-code distribution + over-promise rate
Figure 5: Controlled Experiment — escalation-path intervention (Arm A vs Arm B)
ICLR 2027 submission.
"""
import os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch
import numpy as np
from math import sqrt

# ============================================================================
# Global style (shared by all figures)
# ============================================================================
plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif', 'serif'],
    'font.size': 10,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'axes.linewidth': 0.8,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9,
    'legend.frameon': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.color': '#DDDDDD',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.7,
    'axes.axisbelow': True,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures')
os.makedirs(OUT_DIR, exist_ok=True)

COLORS = {
    'anchored': '#2E7D32',
    'overpromise': '#C62828',
    'unverifiable': '#F9A825',
    'undetermined': '#757575',
    'panel_bg': '#FAFAFA',
    'box_border': '#333333',
    'arrow': '#555555',
}


def wilson_ci(k, n, alpha=0.05):
    """95% Wilson score interval for a binomial proportion."""
    if n == 0:
        return 0.0, 0.0
    z = 1.959963984540054
    phat = k / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    margin = z * sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / denom
    lo = max(0.0, center - margin)
    hi = min(1.0, center + margin)
    return lo, hi


# ============================================================================
# Figure 1: Framework Overview
# ============================================================================
def make_figure_1():
    fig = plt.figure(figsize=(10, 7.5), facecolor='white')

    # === Panel A: Skeleton (top) ===
    ax_a = fig.add_axes([0.08, 0.68, 0.84, 0.26])
    ax_a.set_facecolor('white')
    ax_a.set_xlim(0, 10); ax_a.set_ylim(0, 6); ax_a.axis('off')

    ax_a.text(5, 5.5, 'A  The Skeleton — Traceability', fontsize=13, fontweight='bold', ha='center', va='center')
    ax_a.text(5, 5.0, 'Ground truth: "what was actually called" (self-evidencing, no reference trajectory needed)',
              fontsize=9.5, ha='center', va='center', color='#555555')

    cell_w, cell_h = 3.2, 0.9
    x0, y0 = 1.2, 2.0
    cells = [
        (x0, y0+cell_h, 'Both judge\nas pass', '#E8F5E9'),
        (x0+cell_w, y0+cell_h, 'Traj. accuracy: fail\nOur instrument: pass', '#FFF3E0'),
        (x0, y0, 'Traj. accuracy: pass\nOur instrument: fail', '#FFF3E0'),
        (x0+cell_w, y0, 'Both judge as fail\n(different attribution)', '#FFEBEE'),
    ]
    for x, y, text, color in cells:
        rect = FancyBboxPatch((x, y), cell_w, cell_h, boxstyle="round,pad=0.05",
                               facecolor=color, edgecolor='#CCCCCC', linewidth=0.8)
        ax_a.add_patch(rect)
        ax_a.text(x+cell_w/2, y+cell_h/2, text, fontsize=9, ha='center', va='center')

    ax_a.text(x0-0.4, y0+cell_h*1.5, 'Text\nanchored', fontsize=10, ha='center', va='center', fontweight='bold')
    ax_a.text(x0-0.4, y0+cell_h*0.5, 'Text\nunanchored', fontsize=10, ha='center', va='center', fontweight='bold')
    ax_a.text(x0+cell_w*0.5, y0+cell_h*2.2, 'Tool-call correct', fontsize=10, ha='center', fontweight='bold')
    ax_a.text(x0+cell_w*1.5, y0+cell_h*2.2, 'Tool-call incorrect', fontsize=10, ha='center', fontweight='bold')

    # === Panel B: Skin (middle) ===
    ax_b = fig.add_axes([0.08, 0.40, 0.84, 0.22])
    ax_b.set_facecolor('white')
    ax_b.set_xlim(0, 10); ax_b.set_ylim(0, 4); ax_b.axis('off')

    ax_b.text(5, 3.6, 'B  The Skin — Four-Step Derivation Procedure', fontsize=13, fontweight='bold', ha='center', va='center')

    steps = [
        ('1', 'Tool Registry\nEnumeration', 'action vocabulary T'),
        ('2', 'Business Process\nExtraction', 'commitment semantics'),
        ('3', 'Mapping Rules\nInstantiation', 'statement → action'),
        ('4', 'Alignment Window\n& Exemption Table', 'evolvable criterion'),
    ]
    box_w, box_h = 1.9, 1.5
    start_x, y = 0.5, 0.5

    for i, (num, title, desc) in enumerate(steps):
        x = start_x + i * (box_w + 0.4)
        rect = FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0.08",
                               facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=1.2)
        ax_b.add_patch(rect)
        ax_b.text(x+0.15, y+box_h-0.35, num, fontsize=18, fontweight='bold', color='#1976D2')
        ax_b.text(x+box_w/2, y+box_h*0.5, title, fontsize=9.5, ha='center', va='center', fontweight='bold')
        ax_b.text(x+box_w/2, y+0.2, desc, fontsize=8, ha='center', va='center', color='#555555')
        if i < 3:
            ax_b.annotate('', xy=(x+box_w+0.1, y+box_h/2), xytext=(x+box_w+0.25, y+box_h/2),
                          arrowprops=dict(arrowstyle='->', color='#1976D2', lw=1.5))

    ax_b.text(5, 0.1, 'Steps 1, 3, 4 are fixed across scenarios. Only Step 2 requires domain knowledge.',
              fontsize=9, ha='center', color='#555555', style='italic')

    # === Panel C: Readout States (bottom) ===
    ax_c = fig.add_axes([0.08, 0.08, 0.84, 0.26])
    ax_c.set_facecolor('white')
    ax_c.set_xlim(0, 10); ax_c.set_ylim(0, 4); ax_c.axis('off')

    ax_c.text(5, 3.6, 'C  Four Readout States', fontsize=13, fontweight='bold', ha='center', va='center')

    states = [
        ('Anchored', 'Claim in T, execution exists\nSubtypes: execution & escalation', COLORS['anchored'], '#E8F5E9'),
        ('Over-promise', 'Claim in T, no execution\nCompletive claim of specific action', COLORS['overpromise'], '#FFEBEE'),
        ('Unverifiable', 'Off-session / future / third-party\nCannot be verified within session', COLORS['unverifiable'], '#FFFDE7'),
        ('UNDETERMINED', 'Text empty or unresolvable\nMust never be force-classified', COLORS['undetermined'], '#F5F5F5'),
    ]
    box_w2, box_h2 = 2.1, 1.8
    start_x2, y2 = 0.5, 0.3

    for i, (name, desc, border_color, fill_color) in enumerate(states):
        x = start_x2 + i * (box_w2 + 0.25)
        rect = FancyBboxPatch((x, y2), box_w2, box_h2, boxstyle="round,pad=0.08",
                               facecolor=fill_color, edgecolor=border_color, linewidth=1.5)
        ax_c.add_patch(rect)
        ax_c.text(x+box_w2/2, y2+box_h2-0.35, name, fontsize=11, ha='center', va='center', fontweight='bold',
                  color=border_color)
        ax_c.text(x+box_w2/2, y2+box_h2*0.4, desc, fontsize=8.5, ha='center', va='center', color='#333333')

    out = os.path.join(OUT_DIR, 'fig1_framework.pdf')
    plt.savefig(out)
    plt.close(fig)
    print(f'Saved {out}')


# ============================================================================
# Figure 2: Layered Readout
# ============================================================================
def make_figure_2():
    l1_anchored = 132
    l1_unanchored = 320
    l1_total = l1_anchored + l1_unanchored

    l2 = {
        'Anchored execution': 132,
        'Anchored escalation': 164,
        'Unverifiable': 126,
        'Over-promise': 21,
        'Intentive': 7,
        'UNDETERMINED': 2,
    }
    l2_total = sum(l2.values())

    l2_order = ['Anchored execution', 'Anchored escalation',
                'Unverifiable', 'Intentive', 'Over-promise', 'UNDETERMINED']
    l2_colors = {
        'Anchored execution':   '#2E7D32',
        'Anchored escalation':  '#9CCC65',
        'Unverifiable':         '#F4D03F',
        'Intentive':            '#F0B27A',
        'Over-promise':         '#E74C3C',
        'UNDETERMINED':         '#7F8C8D',
    }

    fig, ax = plt.subplots(figsize=(9.2, 3.4))

    bar_height = 0.34
    y_l1, y_l2 = 1.0, 0.0

    # L1 bar
    left = 0
    for label, val, color in [
        ('Anchored (BV)', l1_anchored, '#2E7D32'),
        ('Unanchored (≠BV)', l1_unanchored, '#BDBDBD'),
    ]:
        ax.barh(y_l1, val, left=left, height=bar_height,
                color=color, edgecolor='white', linewidth=0.6)
        pct = 100.0 * val / l1_total
        if val > 12:
            ax.text(left + val / 2, y_l1,
                    f'{val}\n({pct:.1f}%)',
                    ha='center', va='center', color='white',
                    fontsize=8.5, fontweight='bold', linespacing=1.1)
        left += val

    # L2 bar
    left = 0
    for label in l2_order:
        val = l2[label]
        color = l2_colors[label]
        ax.barh(y_l2, val, left=left, height=bar_height,
                color=color, edgecolor='white', linewidth=0.6)
        pct = 100.0 * val / l2_total
        if val > 14:
            txt_color = 'white' if color in ('#2E7D32', '#E74C3C', '#7F8C8D') else '#222222'
            ax.text(left + val / 2, y_l2,
                    f'{val}\n({pct:.1f}%)',
                    ha='center', va='center', color=txt_color,
                    fontsize=8.2, fontweight='bold', linespacing=1.1)
        elif val > 4:
            ax.text(left + val / 2, y_l2, f'{val}',
                    ha='center', va='center', color='#222222',
                    fontsize=8.0, fontweight='bold')
        left += val

    ax.text(-8, y_l1, 'L1\nDeterministic', ha='right', va='center',
            fontsize=10, fontweight='bold', color='#333333', linespacing=1.1)
    ax.text(-8, y_l2, 'L2\nHuman-adjudicated', ha='right', va='center',
            fontsize=10, fontweight='bold', color='#333333', linespacing=1.1)

    ax.set_yticks([])
    ax.set_xlim(-90, l2_total + 10)
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel('Number of direct-execution texts  (N = 452)', fontsize=10.5)
    ax.set_title('Layered Readout of 452 Direct-Execution Texts',
                 fontsize=12.5, fontweight='bold', pad=12)

    legend_handles = [Patch(facecolor=l2_colors[k], edgecolor='white', label=k) for k in l2_order]
    legend_handles.append(Patch(facecolor='#BDBDBD', edgecolor='white', label='Unanchored (≠BV)'))
    ax.legend(handles=legend_handles, loc='upper center',
              bbox_to_anchor=(0.5, -0.22), ncol=4, fontsize=8.5,
              handlelength=1.4, columnspacing=1.4, handletextpad=0.5)

    ax.grid(axis='y', visible=False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, 'fig2_layered_readout.pdf')
    plt.savefig(out)
    plt.close(fig)
    print(f'Saved {out}')


# ============================================================================
# Figure 3: ITSM Deployment Condition Modulation
# ============================================================================
def make_figure_3():
    data = {
        'GLM-5.2':            {'low': (4, 120),  'high': (48, 120), 'CON': (0, 40),  'STD': (18, 40), 'AGG': (30, 40)},
        'Claude-Haiku-4.5':   {'low': (0, 120),  'high': (13, 120), 'CON': (0, 40),  'STD': (7, 40),  'AGG': (6, 40)},
        'DS-V4-Flash':        {'low': (0, 120),  'high': (21, 120), 'CON': (0, 40),  'STD': (0, 40),  'AGG': (21, 40)},
        'Qwen-Plus':          {'low': (39, 120), 'high': (74, 120), 'CON': (10, 40), 'STD': (24, 40), 'AGG': (40, 40)},
        'Claude-Sonnet-4.6':  {'low': (0, 120),  'high': (0, 120),  'CON': (0, 40),  'STD': (0, 40),  'AGG': (0, 40)},
    }
    models = list(data.keys())
    conditions = ['low', 'high', 'AGG']
    cond_labels = ['Cost Low', 'Cost High', 'AGG posture']
    colors = ['#4C72B0', '#DD8452', '#C44E52']

    n_models = len(models)
    n_cond = len(conditions)
    bar_width = 0.26
    group_gap = 0.25
    group_centers = np.arange(n_models) * (n_cond * bar_width + group_gap)

    fig, ax = plt.subplots(figsize=(9.6, 4.6))

    for ci, (cond, label, color) in enumerate(zip(conditions, cond_labels, colors)):
        offsets = (ci - (n_cond - 1) / 2) * bar_width
        xs = group_centers + offsets

        rates, lo_err, hi_err = [], [], []
        for m in models:
            k, n = data[m][cond]
            rate = k / n
            lo, hi = wilson_ci(k, n)
            rates.append(rate * 100)
            lo_err.append((rate - lo) * 100)
            hi_err.append((hi - rate) * 100)

        ax.bar(xs, rates, width=bar_width, color=color,
               edgecolor='white', linewidth=0.6, label=label, zorder=3)
        ax.errorbar(xs, rates, yerr=[lo_err, hi_err],
                    fmt='none', ecolor='#333333', elinewidth=0.9,
                    capsize=2.5, capthick=0.9, zorder=4)
        for x, r in zip(xs, rates):
            ax.text(x, r + 2.2, f'{r:.1f}%',
                    ha='center', va='bottom', fontsize=7.8, color='#333333')

    ax.set_xticks(group_centers)
    ax.set_xticklabels(models, fontsize=9.5)
    ax.set_ylabel('BV rate (%)', fontsize=11)
    ax.set_ylim(0, 105)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v)}%'))
    ax.set_title('BV Rate by Deployment Condition (ITSM)',
                 fontsize=12.5, fontweight='bold', pad=12)
    ax.legend(loc='upper left', ncol=1, fontsize=9.5,
              title='Condition', title_fontsize=9.5)
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', color='#E2E2E2', linewidth=0.6, alpha=0.9)
    ax.set_axisbelow(True)
    ax.text(0.012, 0.018,
            'Cost Low / Cost High: n = 120 per model   |   AGG posture: n = 40 per model\n'
            'Error bars: 95% Wilson score confidence intervals.',
            transform=ax.transAxes, fontsize=7.8, color='#555555',
            va='bottom', ha='left', linespacing=1.4)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, 'fig3_itsm_modulation.pdf')
    plt.savefig(out)
    plt.close(fig)
    print(f'Saved {out}')


# ============================================================================
# Figure 4: Cross-Scenario Comparison
# ============================================================================
# Data from promise_type_v2.jsonl (direct-execution texts) and paper §4.2 Table 2
# Scenario mapping: D1=Policy Renewal, D3=Contract Amendment, D4=Refund Processing
# ============================================================================
def make_figure_4():
    scenarios = ['Policy\nRenewal', 'Contract\nAmendment', 'Refund\nProcessing']

    # Tool-code counts among direct-execution texts
    code_data = {
        'BV (modification)': [115, 7, 25],
        'AE (escalation)':   [0, 101, 175],
        'AR (refusal)':      [5, 13, 16],
        'CS (query)':        [11, 0, 0],
    }
    totals = [131, 121, 216]

    # Over-promise counts and rates from paper §4.2
    op_counts = [13, 2, 6]
    op_rates = [11.3, 1.7, 2.8]
    op_cis = [(6.7, 18.4), (0.5, 5.8), (1.3, 5.9)]

    colors = {
        'BV (modification)': '#C44E52',
        'AE (escalation)':   '#4C72B0',
        'AR (refusal)':      '#7F8C8D',
        'CS (query)':        '#F4D03F',
    }
    code_order = ['BV (modification)', 'AE (escalation)', 'AR (refusal)', 'CS (query)']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2),
                                    gridspec_kw={'width_ratios': [1.8, 1]})

    # ---- Left panel: Stacked bar (tool-code distribution) ----
    x = np.arange(len(scenarios))
    bar_width = 0.55
    bottom = np.zeros(len(scenarios))

    for code in code_order:
        vals = np.array(code_data[code])
        ax1.bar(x, vals, bar_width, bottom=bottom,
                color=colors[code], edgecolor='white', linewidth=0.6,
                label=code, zorder=3)
        bottom += vals

    for i, total in enumerate(totals):
        ax1.text(i, total + 6, f'n={total}',
                 ha='center', va='bottom', fontsize=9, fontweight='bold', color='#333333')

    bottom_check = np.zeros(len(scenarios))
    for code in code_order:
        vals = np.array(code_data[code])
        for i, v in enumerate(vals):
            if v > 15:
                pct = 100.0 * v / totals[i]
                txt_color = 'white' if code in ['BV (modification)', 'AE (escalation)'] else '#222222'
                ax1.text(i, bottom_check[i] + v/2, f'{v}\n({pct:.0f}%)',
                         ha='center', va='center', fontsize=7.8,
                         color=txt_color, fontweight='bold', linespacing=1.1)
        bottom_check += vals

    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, fontsize=9.5)
    ax1.set_ylabel('Number of direct-execution texts', fontsize=10.5)
    ax1.set_title('Tool-Code Distribution\nAmong Direct-Execution Texts',
                  fontsize=11.5, fontweight='bold', pad=10)
    ax1.set_ylim(0, max(totals) * 1.18)
    ax1.legend(loc='upper right', fontsize=8.5, handlelength=1.2)
    ax1.grid(axis='x', visible=False)

    # ---- Right panel: Over-promise rate with 95% CI ----
    x2 = np.arange(len(scenarios))
    bar_width2 = 0.5
    op_lo = [r - lo for r, (lo, hi) in zip(op_rates, op_cis)]
    op_hi = [hi - r for r, (lo, hi) in zip(op_rates, op_cis)]

    ax2.bar(x2, op_rates, bar_width2,
            color='#C44E52', edgecolor='white', linewidth=0.6, alpha=0.85, zorder=3)
    ax2.errorbar(x2, op_rates, yerr=[op_lo, op_hi],
                 fmt='none', ecolor='#333333', elinewidth=0.9,
                 capsize=3, capthick=0.9, zorder=4)

    for i, (rate, count, total) in enumerate(zip(op_rates, op_counts, [115, 121, 216])):
        ax2.text(i, rate + 0.7, f'{rate:.1f}%\n({count}/{total})',
                 ha='center', va='bottom', fontsize=8.5,
                 color='#C44E52', fontweight='bold', linespacing=1.2)

    ax2.set_xticks(x2)
    ax2.set_xticklabels(scenarios, fontsize=9.5)
    ax2.set_ylabel('Over-promise rate (%)', fontsize=10.5)
    ax2.set_title('Over-Promise Rate\nby Scenario (L2, Human-Adjudicated)',
                  fontsize=11.5, fontweight='bold', pad=10)
    ax2.set_ylim(0, 22)
    ax2.grid(axis='x', visible=False)
    ax2.text(0.98, 0.98, '95% Wilson CI',
             transform=ax2.transAxes, fontsize=7.5, color='#555555',
             va='top', ha='right', style='italic')

    plt.tight_layout()
    out = os.path.join(OUT_DIR, 'fig4_cross_scenario.pdf')
    plt.savefig(out)
    plt.close(fig)
    print(f'Saved {out}')


# ============================================================================
# Figure 5: Controlled Experiment — Escalation Path Intervention
# ============================================================================
# Data from paper §4.2 controlled variant:
# Arm A (no ticket tool) vs Arm B (with ticket tool), 120 seeds per model per arm
# ============================================================================
def make_figure_5():
    models = ['GPT-5.4', 'Qwen-Plus', 'DS-V4-Flash']
    n = 120

    arm_a_counts = [19, 116, 112]
    arm_b_counts = [0, 117, 114]

    arm_a_rates = [c/n * 100 for c in arm_a_counts]
    arm_b_rates = [c/n * 100 for c in arm_b_counts]

    arm_a_cis = [wilson_ci(c, n) for c in arm_a_counts]
    arm_b_cis = [wilson_ci(c, n) for c in arm_b_counts]

    fig, ax = plt.subplots(figsize=(7.5, 4.8))

    x = np.arange(len(models))
    bar_width = 0.32
    gap = 0.04

    # Arm A
    a_lo = [r - lo*100 for r, (lo, hi) in zip(arm_a_rates, arm_a_cis)]
    a_hi = [hi*100 - r for r, (lo, hi) in zip(arm_a_rates, arm_a_cis)]
    ax.bar(x - bar_width/2 - gap/2, arm_a_rates, bar_width,
           color='#DD8452', edgecolor='white', linewidth=0.6,
           label='Arm A: No ticket tool', zorder=3)
    ax.errorbar(x - bar_width/2 - gap/2, arm_a_rates,
                yerr=[a_lo, a_hi], fmt='none',
                ecolor='#333333', elinewidth=0.9, capsize=2.5, capthick=0.9, zorder=4)

    # Arm B
    b_lo = [r - lo*100 for r, (lo, hi) in zip(arm_b_rates, arm_b_cis)]
    b_hi = [hi*100 - r for r, (lo, hi) in zip(arm_b_rates, arm_b_cis)]
    ax.bar(x + bar_width/2 + gap/2, arm_b_rates, bar_width,
           color='#4C72B0', edgecolor='white', linewidth=0.6,
           label='Arm B: With ticket tool', zorder=3)
    ax.errorbar(x + bar_width/2 + gap/2, arm_b_rates,
                yerr=[b_lo, b_hi], fmt='none',
                ecolor='#333333', elinewidth=0.9, capsize=2.5, capthick=0.9, zorder=4)

    # Value labels
    for i in range(len(models)):
        ax.text(x[i] - bar_width/2 - gap/2, arm_a_rates[i] + 2.5,
                f'{arm_a_rates[i]:.1f}%', ha='center', va='bottom',
                fontsize=8.5, fontweight='bold', color='#DD8452')
        ax.text(x[i] + bar_width/2 + gap/2, arm_b_rates[i] + 2.5,
                f'{arm_b_rates[i]:.1f}%', ha='center', va='bottom',
                fontsize=8.5, fontweight='bold', color='#4C72B0')

    # Annotation for GPT-5.4's significant drop
    ax.annotate('p < 0.001\n(Fisher exact)',
                xy=(0, 0), xytext=(0, 30),
                ha='center', fontsize=8, color='#C44E52', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#C44E52', lw=1.2))

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10)
    ax.set_ylabel('BV rate (%)', fontsize=11)
    ax.set_title('Effect of Escalation-Path Availability\non Tool-Layer Violation Rate',
                 fontsize=12, fontweight='bold', pad=12)
    ax.set_ylim(0, 112)
    ax.set_yticks(np.arange(0, 101, 20))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v)}%'))
    ax.legend(loc='upper left', fontsize=9, handlelength=1.4)
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', color='#E2E2E2', linewidth=0.6, alpha=0.9)

    ax.text(0.012, 0.015,
            'n = 120 per model per arm   |   Error bars: 95% Wilson CI\n'
            'Scenario: Policy Renewal, STD and AGG posture\n'
            'Arm B adds create_renewal_request tool + one rule to the registry',
            transform=ax.transAxes, fontsize=7.5, color='#555555',
            va='bottom', ha='left', linespacing=1.4)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, 'fig5_controlled_experiment.pdf')
    plt.savefig(out)
    plt.close(fig)
    print(f'Saved {out}')


# ============================================================================
if __name__ == '__main__':
    make_figure_1()
    make_figure_2()
    make_figure_3()
    make_figure_4()
    make_figure_5()
    print('All 5 figures generated.')