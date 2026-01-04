//
//  App.swift
//  MathSymbolRecognizer
//
//  macOS MVP for Intelligent Handwritten Math Recognition
//

import SwiftUI

@main
struct MathSymbolRecognizerApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowStyle(.automatic)
        .commands {
            CommandGroup(replacing: .newItem) {}
        }
    }
}

