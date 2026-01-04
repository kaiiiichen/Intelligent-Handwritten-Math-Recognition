//
//  SettingsView.swift
//  MathSymbolRecognizer
//
//  Settings and preferences interface
//

import SwiftUI

struct SettingsView: View {
    @ObservedObject private var preferences = UserPreferences.shared
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Settings")
                .font(.title2)
                .fontWeight(.semibold)
            
            GroupBox("Recognition") {
                VStack(alignment: .leading, spacing: 12) {
                    Toggle("Auto-recognize after drawing", isOn: $preferences.autoRecognitionEnabled)
                        .help("Automatically recognize symbols after you stop drawing")
                    
                    if preferences.autoRecognitionEnabled {
                        HStack {
                            Text("Delay:")
                            Slider(value: $preferences.autoRecognitionDelay, in: 0.5...3.0, step: 0.1) {
                                Text("Auto-recognition delay")
                            }
                            Text("\(preferences.autoRecognitionDelay, specifier: "%.1f")s")
                                .frame(width: 40)
                                .font(.system(.body, design: .monospaced))
                        }
                        .help("How long to wait after you stop drawing before auto-recognizing")
                    }
                }
                .padding(.vertical, 8)
            }
            
            GroupBox("Personalization") {
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        Text("Choice history:")
                        Spacer()
                        Button("Clear History") {
                            showingClearConfirmation = true
                        }
                        .foregroundColor(.red)
                    }
                    
                    Text("The app remembers your LaTeX command choices to show \"last chosen\" markers.")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding(.vertical, 8)
            }
            
            Spacer()
            
            HStack {
                Spacer()
                Button("Done") {
                    dismiss()
                }
                .keyboardShortcut(.return, modifiers: [])
            }
        }
        .padding(20)
        .frame(width: 400, height: 300)
        .alert("Clear Choice History", isPresented: $showingClearConfirmation) {
            Button("Cancel", role: .cancel) { }
            Button("Clear", role: .destructive) {
                preferences.clearHistory()
            }
        } message: {
            Text("This will remove all \"last chosen\" markers. This action cannot be undone.")
        }
    }
    
    @State private var showingClearConfirmation = false
}

#Preview {
    SettingsView()
}