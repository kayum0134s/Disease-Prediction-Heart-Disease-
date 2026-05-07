"""
CardioPredict — PDF Medical Report Generator
Generates a professional medical report using ReportLab.
"""
import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Color palette
C_DARK      = colors.HexColor('#050b1f')
C_NEON_BLUE = colors.HexColor('#00d4ff')
C_NEON_RED  = colors.HexColor('#ff2d55')
C_PANEL     = colors.HexColor('#0d1b3e')
C_TEXT      = colors.HexColor('#ccd6f6')
C_SUBTEXT   = colors.HexColor('#8892b0')
C_WHITE     = colors.white
C_LOW       = colors.HexColor('#00ff88')
C_MOD       = colors.HexColor('#ffd60a')
C_HIGH      = colors.HexColor('#ff9500')
C_CRIT      = colors.HexColor('#ff2d55')

RISK_COLORS = {
    'low': C_LOW, 'moderate': C_MOD, 'high': C_HIGH, 'critical': C_CRIT
}

CP_LABELS  = {0: 'Typical Angina', 1: 'Atypical Angina', 2: 'Non-Anginal Pain', 3: 'Asymptomatic'}
ECG_LABELS = {0: 'Normal', 1: 'ST-T Abnormality', 2: 'LV Hypertrophy'}
THAL_LABELS= {1: 'Normal', 2: 'Fixed Defect', 3: 'Reversible Defect'}
SLOPE_LABELS={0: 'Upsloping', 1: 'Flat', 2: 'Downsloping'}


def generate_pdf(patient_data: dict) -> bytes:
    """
    patient_data: dict from db.get_patient_by_id()
    Returns: PDF as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=15*mm, bottomMargin=15*mm
    )

    styles = getSampleStyleSheet()

    def style(name, **kwargs):
        return ParagraphStyle(name, **kwargs)

    s_title   = style('title',   fontName='Helvetica-Bold', fontSize=22, textColor=C_NEON_BLUE,  alignment=TA_CENTER, spaceAfter=2)
    s_sub     = style('sub',     fontName='Helvetica',      fontSize=10, textColor=C_SUBTEXT,    alignment=TA_CENTER, spaceAfter=6)
    s_section = style('section', fontName='Helvetica-Bold', fontSize=12, textColor=C_NEON_BLUE,  spaceBefore=10, spaceAfter=4)
    s_body    = style('body',    fontName='Helvetica',       fontSize=10, textColor=C_TEXT,       spaceAfter=3)
    s_risk    = style('risk',    fontName='Helvetica-Bold', fontSize=18, textColor=C_NEON_RED,   alignment=TA_CENTER, spaceAfter=4)
    s_small   = style('small',   fontName='Helvetica',      fontSize=8,  textColor=C_SUBTEXT)

    story = []

    # ── Header ─────────────────────────────────────────────────
    story.append(Paragraph('CardioPredict', s_title))
    story.append(Paragraph('AI-Powered Cardiovascular Risk Assessment Report', s_sub))
    story.append(HRFlowable(width='100%', thickness=1, color=C_NEON_BLUE))
    story.append(Spacer(1, 8))

    # ── Report meta ────────────────────────────────────────────
    meta_data = [
        ['Patient ID', f"CP-{patient_data.get('id', '—'):04d}",
         'Report Date', datetime.now().strftime('%d %b %Y, %H:%M')],
        ['Patient Name', patient_data.get('name', '—'),
         'Assessed By', 'CardioPredict AI Engine v2.0'],
    ]
    meta_table = Table(meta_data, colWidths=[35*mm, 65*mm, 35*mm, 55*mm])
    meta_table.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('TEXTCOLOR',  (0,0), (-1,-1), C_TEXT),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',   (2,0), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR',  (0,0), (0,-1), C_NEON_BLUE),
        ('TEXTCOLOR',  (2,0), (2,-1), C_NEON_BLUE),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [C_PANEL, C_DARK]),
        ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor('#1a2a4a')),
        ('TOPPADDING',  (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # ── Diagnosis Result ───────────────────────────────────────
    story.append(Paragraph('Diagnosis Result', s_section))
    pred_label = patient_data.get('prediction_label') or (
        'Heart Disease Detected' if patient_data.get('prediction') == 1 else 'No Heart Disease'
    )
    risk_pct   = patient_data.get('risk_score', 0)
    risk_band  = patient_data.get('risk_label', 'Unknown')
    risk_key   = patient_data.get('risk_band', 'low')
    risk_color = RISK_COLORS.get(risk_key, C_MOD)

    diag_data = [
        ['Final Prediction', pred_label],
        ['Risk Score',       f"{risk_pct}%"],
        ['Risk Category',    risk_band],
    ]
    diag_table = Table(diag_data, colWidths=[60*mm, 130*mm])
    diag_table.setStyle(TableStyle([
        ('FONTNAME',   (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 11),
        ('TEXTCOLOR',  (0,0), (0,-1), C_NEON_BLUE),
        ('TEXTCOLOR',  (1,0), (1,-1), C_WHITE),
        ('TEXTCOLOR',  (1,2), (1,2),  risk_color),
        ('FONTNAME',   (1,2), (1,2),  'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,-1), C_PANEL),
        ('GRID',       (0,0), (-1,-1), 0.3, colors.HexColor('#1a2a4a')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
    ]))
    story.append(diag_table)
    story.append(Spacer(1, 10))

    # ── Model Comparison ──────────────────────────────────────
    story.append(Paragraph('ML Model Comparison', s_section))
    inp = patient_data.get('inputs', {})
    model_rows = [
        ['Model', 'Risk Probability', 'Prediction'],
        ['Logistic Regression', f"{patient_data.get('lr_prob', 0):.1f}%",
         'Positive' if (patient_data.get('lr_prob') or 0) >= 50 else 'Negative'],
        ['Random Forest (Final)', f"{patient_data.get('rf_prob', 0):.1f}%",
         'Positive' if (patient_data.get('rf_prob') or 0) >= 50 else 'Negative'],
        ['SVM', f"{patient_data.get('svm_prob', 0):.1f}%",
         'Positive' if (patient_data.get('svm_prob') or 0) >= 50 else 'Negative'],
    ]
    model_table = Table(model_rows, colWidths=[80*mm, 60*mm, 50*mm])
    model_table.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,0), (-1,-1), 10),
        ('TEXTCOLOR',   (0,0), (-1,0),  C_DARK),
        ('BACKGROUND',  (0,0), (-1,0),  C_NEON_BLUE),
        ('TEXTCOLOR',   (0,1), (-1,-1), C_TEXT),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_PANEL, C_DARK]),
        ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor('#1a2a4a')),
        ('TOPPADDING',  (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('ALIGN',       (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(model_table)
    story.append(Spacer(1, 10))

    # ── Patient Parameters ────────────────────────────────────
    story.append(Paragraph('Patient Medical Parameters', s_section))
    sex_label = 'Male' if str(inp.get('sex','')) == '1' else 'Female'
    param_data = [
        ['Parameter',          'Value', 'Parameter',       'Value'],
        ['Age',                f"{inp.get('age','—')} years",
         'Chest Pain Type',   CP_LABELS.get(int(inp.get('cp',0)), '—')],
        ['Sex',                sex_label,
         'Exercise Angina',   'Yes' if inp.get('exang') else 'No'],
        ['Resting BP',         f"{inp.get('trestbps','—')} mmHg",
         'ST Depression',     str(inp.get('oldpeak','—'))],
        ['Cholesterol',        f"{inp.get('chol','—')} mg/dl",
         'Slope',             SLOPE_LABELS.get(int(inp.get('slope',0)),'—')],
        ['Fasting Blood Sugar',f"{'> 120 mg/dl' if inp.get('fbs') else '≤ 120 mg/dl'}",
         'Major Vessels (CA)',str(inp.get('ca','—'))],
        ['Resting ECG',        ECG_LABELS.get(int(inp.get('restecg',0)),'—'),
         'Thalassemia',       THAL_LABELS.get(int(inp.get('thal',1)),'—')],
        ['Max Heart Rate',     f"{inp.get('thalach','—')} bpm",
         '',                  ''],
    ]
    param_table = Table(param_data, colWidths=[50*mm, 45*mm, 55*mm, 40*mm])
    param_table.setStyle(TableStyle([
        ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
        ('BACKGROUND',  (0,0), (-1,0),  C_PANEL),
        ('TEXTCOLOR',   (0,0), (-1,0),  C_NEON_BLUE),
        ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('TEXTCOLOR',   (0,1), (-1,-1), C_TEXT),
        ('FONTNAME',    (0,1), (0,-1),  'Helvetica-Bold'),
        ('FONTNAME',    (2,1), (2,-1),  'Helvetica-Bold'),
        ('TEXTCOLOR',   (0,1), (0,-1),  C_SUBTEXT),
        ('TEXTCOLOR',   (2,1), (2,-1),  C_SUBTEXT),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_DARK, C_PANEL]),
        ('GRID',        (0,0), (-1,-1), 0.3, colors.HexColor('#1a2a4a')),
        ('TOPPADDING',  (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 10))

    # ── Health Recommendations ────────────────────────────────
    story.append(Paragraph('Personalized Health Recommendations', s_section))
    recs = patient_data.get('recommendations', [])
    for i, rec in enumerate(recs, 1):
        story.append(Paragraph(f'{i}. {rec}', s_body))
    story.append(Spacer(1, 10))

    # ── Disclaimer ────────────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=0.5, color=C_SUBTEXT))
    story.append(Spacer(1, 4))
    disclaimer = (
        "<b>Disclaimer:</b> This report is generated by the CardioPredict AI system "
        "for educational and research purposes only. It does not constitute a medical "
        "diagnosis. Please consult a qualified healthcare professional for clinical decisions."
    )
    story.append(Paragraph(disclaimer, s_small))

    doc.build(story)
    return buffer.getvalue()
