//
//  ContentView.swift
//  MathSymbolRecognizer
//
//  Main view with drawing canvas and suggestion list
//

import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = RecognitionViewModel()
    @State private var showingSettings = false
    
    var body: some View {
        HSplitView {
            // Left side: Drawing canvas
            VStack(spacing: 16) {
                HStack {
                    Text("Draw a Mathematical Symbol")
                        .font(.headline)
                    
                    Spacer()
                    
                    Button(action: {
                        showingSettings = true
                    }) {
                        Image(systemName: "gear")
                    }
                    .buttonStyle(.borderless)
                    .help("Settings")
                }
                .padding(.top)
                .padding(.horizontal)
                
                DrawingCanvasView(viewModel: viewModel)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .background(Color(NSColor.controlBackgroundColor))
                    .cornerRadius(8)
                    .padding(.horizontal)
                
                HStack {
                    Button("Clear") {
                        viewModel.clearDrawing()
                    }
                    .keyboardShortcut(.delete, modifiers: [])
                    
                    Spacer()
                    
                    if UserPreferences.shared.autoRecognitionEnabled {
                        Text("Auto-recognition: ON")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    
                    Spacer()
                    
                    Button("Recognize") {
                        viewModel.recognizeSymbol()
                    }
                    .keyboardShortcut(.return, modifiers: [])
                    .disabled(viewModel.isProcessing)
                }
                .padding(.horizontal)
            }
            .frame(minWidth: 400)
            
            // Right side: Suggestion list
            SuggestionListView(viewModel: viewModel)
                .frame(minWidth: 400)
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView()
        }
    }
}

#Preview {
    ContentView()
}

