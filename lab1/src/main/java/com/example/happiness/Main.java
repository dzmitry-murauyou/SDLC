package com.example.happiness;

import com.example.happiness.controller.HappinessController;
import com.example.happiness.model.HappinessModel;
import com.example.happiness.view.MainFrame;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;

public final class Main {

    private Main() {
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            useSystemLookAndFeel();

            HappinessModel model = new HappinessModel();
            MainFrame mainFrame = new MainFrame();
            HappinessController controller = new HappinessController(model, mainFrame);

            mainFrame.setController(controller);
            model.addPropertyChangeListener(mainFrame); // View слушает активную модель

            mainFrame.setVisible(true);
        });
    }

    private static void useSystemLookAndFeel() {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            System.err.println("Не удалось включить системный LookAndFeel: " + e.getMessage());
        }
    }
}
