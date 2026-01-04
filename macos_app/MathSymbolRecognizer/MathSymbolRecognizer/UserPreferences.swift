//
//  UserPreferences.swift
//  MathSymbolRecognizer
//
//  User preferences and choice history management
//

import Foundation

class UserPreferences: ObservableObject {
    static let shared = UserPreferences()
    
    @Published var autoRecognitionEnabled: Bool {
        didSet {
            UserDefaults.standard.set(autoRecognitionEnabled, forKey: "autoRecognitionEnabled")
        }
    }
    
    @Published var autoRecognitionDelay: Double {
        didSet {
            UserDefaults.standard.set(autoRecognitionDelay, forKey: "autoRecognitionDelay")
        }
    }
    
    private var choiceHistory: [String: String] = [:] // symbolId -> lastChosenLatex
    
    private init() {
        // Load preferences
        self.autoRecognitionEnabled = UserDefaults.standard.object(forKey: "autoRecognitionEnabled") as? Bool ?? true
        self.autoRecognitionDelay = UserDefaults.standard.object(forKey: "autoRecognitionDelay") as? Double ?? 1.0
        
        // Load choice history
        if let historyData = UserDefaults.standard.data(forKey: "choiceHistory"),
           let history = try? JSONDecoder().decode([String: String].self, from: historyData) {
            self.choiceHistory = history
        }
    }
    
    /// Record user's choice for a symbol
    func recordChoice(symbolId: Int, latexCommand: String) {
        let key = String(symbolId)
        choiceHistory[key] = latexCommand
        saveChoiceHistory()
        
        print("📝 Recorded choice: Symbol \(symbolId) -> \(latexCommand)")
    }
    
    /// Get last chosen LaTeX command for a symbol
    func getLastChoice(symbolId: Int) -> String? {
        let key = String(symbolId)
        return choiceHistory[key]
    }
    
    /// Check if a LaTeX command was the last choice for any symbol
    func isLastChosen(latexCommand: String) -> Bool {
        return choiceHistory.values.contains(latexCommand)
    }
    
    /// Clear all choice history
    func clearHistory() {
        choiceHistory.removeAll()
        saveChoiceHistory()
    }
    
    /// Export choice history
    func exportHistory() -> [String: String] {
        return choiceHistory
    }
    
    /// Import choice history
    func importHistory(_ history: [String: String]) {
        self.choiceHistory = history
        saveChoiceHistory()
    }
    
    private func saveChoiceHistory() {
        if let data = try? JSONEncoder().encode(choiceHistory) {
            UserDefaults.standard.set(data, forKey: "choiceHistory")
        }
    }
}

// MARK: - Auto Recognition Timer

class AutoRecognitionTimer: ObservableObject {
    private var timer: Timer?
    private var completion: (() -> Void)?
    
    func schedule(delay: TimeInterval, completion: @escaping () -> Void) {
        cancel() // Cancel any existing timer
        
        self.completion = completion
        self.timer = Timer.scheduledTimer(withTimeInterval: delay, repeats: false) { _ in
            completion()
        }
    }
    
    func cancel() {
        timer?.invalidate()
        timer = nil
        completion = nil
    }
    
    deinit {
        cancel()
    }
}