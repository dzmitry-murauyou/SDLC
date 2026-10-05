package com.example.happiness.view;

import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.DocumentFilter;


final class NumericDocumentFilter extends DocumentFilter {

    interface RejectListener {
        void onRejectedText(String attemptedText);
    }

    private final boolean allowDecimal;
    private final RejectListener listener;

    NumericDocumentFilter(boolean allowDecimal, RejectListener listener) {
        this.allowDecimal = allowDecimal;
        this.listener = listener;
    }

    @Override
    public void replace(FilterBypass fb, int offset, int length, String text, AttributeSet attrs)
            throws BadLocationException {
        if (text == null || text.isEmpty()) {
            super.replace(fb, offset, length, "", attrs);
            return;
        }
        String current = fb.getDocument().getText(0, fb.getDocument().getLength());
        StringBuilder sb = new StringBuilder(current);
        sb.replace(offset, offset + length, text);
        if (isAcceptable(sb.toString())) {
            super.replace(fb, offset, length, text, attrs);
        } else if (listener != null) {
            listener.onRejectedText(text);
        }
    }

    private boolean isAcceptable(String candidate) {
        if (candidate.isEmpty()) {
            return true;
        }
        if (!allowDecimal) {
            return candidate.matches("\\d*");
        }
        return candidate.matches("\\d*[.,]?\\d*");
    }
}
