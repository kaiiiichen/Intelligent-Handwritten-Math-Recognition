//
//  SuggestionListView.swift
//  MathSymbolRecognizer
//
//  Display ranked LaTeX candidate suggestions
//

import SwiftUI
import AppKit

struct SuggestionListView: View {
    @ObservedObject var viewModel: RecognitionViewModel
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text("Suggestions")
                    .font(.headline)
                
                Spacer()
                
                if !viewModel.suggestions.isEmpty {
                    Text("Press 1-5 to select")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }
            .padding()
            
            if viewModel.isProcessing {
                VStack(spacing: 12) {
                    ProgressView()
                        .scaleEffect(0.8)
                    Text("Recognizing symbol...")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if viewModel.suggestions.isEmpty {
                VStack(spacing: 12) {
                    Image(systemName: "pencil.and.outline")
                        .font(.system(size: 32))
                        .foregroundColor(.secondary)
                    
                    VStack(spacing: 4) {
                        Text("Draw a symbol to see suggestions")
                            .foregroundColor(.secondary)
                        
                        if UserPreferences.shared.autoRecognitionEnabled {
                            Text("Auto-recognition is enabled")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        } else {
                            Text("Click 'Recognize' when done")
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                List(Array(viewModel.suggestions.enumerated()), id: \.element.id) { index, suggestion in
                    SuggestionRow(suggestion: suggestion, viewModel: viewModel, index: index + 1)
                        .onTapGesture {
                            viewModel.selectSuggestion(suggestion)
                        }
                }
                .onKeyPress(.digit1) { viewModel.selectSuggestionByIndex(0); return .handled }
                .onKeyPress(.digit2) { viewModel.selectSuggestionByIndex(1); return .handled }
                .onKeyPress(.digit3) { viewModel.selectSuggestionByIndex(2); return .handled }
                .onKeyPress(.digit4) { viewModel.selectSuggestionByIndex(3); return .handled }
                .onKeyPress(.digit5) { viewModel.selectSuggestionByIndex(4); return .handled }
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct SuggestionRow: View {
    let suggestion: Suggestion
    let viewModel: RecognitionViewModel
    let index: Int
    
    var body: some View {
        HStack(spacing: 12) {
            // Number indicator
            Text("\(index)")
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)
                .frame(width: 20, height: 20)
                .background(Color(NSColor.controlBackgroundColor))
                .clipShape(Circle())
            
            // LaTeX preview using our renderer
            LaTeXPreview(suggestion.latexCommand, size: CGSize(width: 40, height: 40))
                .background(Color(NSColor.controlBackgroundColor))
                .cornerRadius(4)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(suggestion.latexCommand)
                    .font(.system(.body, design: .monospaced))
                    .fontWeight(.medium)
                
                HStack(spacing: 8) {
                    Text("Confidence: \(Int(suggestion.confidence * 100))%")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    if suggestion.isLastChosen {
                        HStack(spacing: 2) {
                            Image(systemName: "star.fill")
                                .font(.caption2)
                                .foregroundColor(.orange)
                            Text("last chosen")
                                .font(.caption2)
                                .foregroundColor(.orange)
                        }
                    }
                }
            }
            
            Spacer()
            
            Button(action: {
                viewModel.selectSuggestion(suggestion)
            }) {
                Image(systemName: "doc.on.doc")
            }
            .buttonStyle(.borderless)
            .help("Copy to clipboard")
        }
        .padding(.vertical, 6)
        .padding(.horizontal, 4)
        .background(Color.clear)
        .cornerRadius(6)
        .onHover { isHovered in
            // Add subtle hover effect
        }
    }
}

#Preview {
    SuggestionListView(viewModel: RecognitionViewModel())
}

