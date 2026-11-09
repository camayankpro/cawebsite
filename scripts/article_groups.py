"""Grouping rules for article pages. Shared by the generators."""
import re

GROUP_RULES = [
    ('tds', '^article-tds-'),
    ('audit', '^article-(audit|statutory|internal-audit|tax-audit|bank-audit|stock-audit|management-audit|gst-audit)'),
    ('payroll', '^article-(payroll|pf-esi|professional-tax|gratuity|salary-slips)'),
    ('loans', '^article-(business-loan|loan-consultancy|legal-agreements|real-estate|pan-card|pan-)'),
    ('itr', '^article-(itr-|individual-itr|income-tax|section-80c|new-vs-old|huf-|nri-taxation|capital-gains)'),
    ('gst', '^article-(gst-|ecommerce-gst|export-lut|eway-bill|e-invoicing|input-tax-credit|lut-filing|restaurant-gst)'),
    ('industry', '^article-industry-'),
    ('company', '^article-(company-|llp-|partnership-|proprietorship|opc-|section8|private-limited|roc-|director-|din-|digital-signature|share-transfer|charge-|board-resolutions|moa-aoa|registered-office|startup-india|copyright|trademark-|patent|fssai|iso-|trade-license|msme-|iec-|import-export|business-valuation|fund-raising|outsourced|ccfs)'),
    ('accounting', '^article-(accounting-|accounts-|bank-reconciliation|cash-flow|financial-statements|regular-bookkeeping|mis-reporting|projected-financials|virtual-cfo|working-capital|ca-|form-15ca|financial)'),
]
DEFAULT_GROUP = 'other'

def group_for(filename):
    for group, pattern in GROUP_RULES:
        if re.match(pattern, filename):
            return group
    return DEFAULT_GROUP
