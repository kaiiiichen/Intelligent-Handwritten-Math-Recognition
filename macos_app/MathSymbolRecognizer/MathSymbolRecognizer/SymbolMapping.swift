//
//  SymbolMapping.swift
//  MathSymbolRecognizer
//
//  Symbol ID to LaTeX command mapping
//  Handles index-to-symbol_id mapping from model output
//

import Foundation

struct LaTeXCandidate {
    let command: String
    let mathPriority: Float
    let context: String?
    let description: String?
}

struct SymbolMapping {
    static let shared = SymbolMapping()
    
    // Index (from model output 0-368) -> Symbol ID (from dataset)
    private var idxToSymbolId: [Int: Int] = [:]
    
    // Symbol ID -> LaTeX command (simple mapping, for backward compatibility)
    private var symbolIdToLatex: [Int: String] = [:]
    
    // Symbol ID -> List of LaTeX candidates with math priority
    private var symbolIdToCandidates: [Int: [LaTeXCandidate]] = [:]
    
    init() {
        loadMapping()
    }
    
    private mutating func loadMapping() {
        // First try to load full mapping with math priority (preferred)
        if let fullMappingURL = Bundle.main.url(forResource: "symbol_mapping_full", withExtension: "json") {
            loadFullMapping(path: fullMappingURL.path)
            // Also load index mapping if available
            if let jsonURL = Bundle.main.url(forResource: "symbol_mapping", withExtension: "json") {
                loadIndexMapping(path: jsonURL.path)
            }
        }
        // Fallback: try to load from simple JSON file (includes index mapping)
        else if let jsonURL = Bundle.main.url(forResource: "symbol_mapping", withExtension: "json") {
            loadFromJSON(path: jsonURL.path)
        }
        // Fallback: try to load from CSV
        else if let csvURL = Bundle.main.url(forResource: "symbols", withExtension: "csv") {
            loadFromCSV(path: csvURL.path)
        } else {
            // Last resort: use hardcoded common symbols
            loadCommonSymbols()
            print("⚠️ No mapping file found, using common symbols only")
        }
    }
    
    private mutating func loadFullMapping(path: String) {
        guard let data = try? Data(contentsOf: URL(fileURLWithPath: path)),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            print("❌ Failed to parse symbol_mapping_full.json")
            return
        }
        
        var loadedCount = 0
        for (key, value) in json {
            guard let symbolId = Int(key),
                  let symbolData = value as? [String: Any],
                  let candidatesData = symbolData["latex_candidates"] as? [[String: Any]] else {
                continue
            }
            
            var candidates: [LaTeXCandidate] = []
            for candData in candidatesData {
                guard let command = candData["command"] as? String,
                      let priority = candData["math_priority"] as? Double else {
                    continue
                }
                let context = candData["context"] as? String
                let description = candData["description"] as? String
                
                candidates.append(LaTeXCandidate(
                    command: command,
                    mathPriority: Float(priority),
                    context: context,
                    description: description
                ))
                
                // Also populate simple mapping (use first candidate as default)
                if symbolIdToLatex[symbolId] == nil {
                    symbolIdToLatex[symbolId] = command
                }
            }
            
            // Sort candidates by math priority (descending)
            candidates.sort { $0.mathPriority > $1.mathPriority }
            symbolIdToCandidates[symbolId] = candidates
            loadedCount += 1
        }
        
        print("✅ Loaded \(loadedCount) symbol mappings with math priority from symbol_mapping_full.json")
    }
    
    private mutating func loadIndexMapping(path: String) {
        guard let data = try? Data(contentsOf: URL(fileURLWithPath: path)),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let idxToId = json["idx_to_id"] as? [String: Int] else {
            return
        }
        
        for (key, value) in idxToId {
            if let idx = Int(key) {
                self.idxToSymbolId[idx] = value
            }
        }
        
        print("✅ Loaded \(idxToSymbolId.count) index mappings")
    }
    
    private mutating func loadFromJSON(path: String) {
        guard let data = try? Data(contentsOf: URL(fileURLWithPath: path)),
              let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let idxToId = json["idx_to_id"] as? [String: Int],
              let idToLatex = json["id_to_latex"] as? [String: String] else {
            print("❌ Failed to parse symbol_mapping.json")
            loadCommonSymbols()
            return
        }
        
        // Convert string keys to Int keys
        for (key, value) in idxToId {
            if let idx = Int(key) {
                self.idxToSymbolId[idx] = value
            }
        }
        
        for (key, value) in idToLatex {
            if let id = Int(key) {
                self.symbolIdToLatex[id] = value
            }
        }
        
        print("✅ Loaded \(idxToSymbolId.count) index mappings and \(symbolIdToLatex.count) LaTeX mappings from JSON")
    }
    
    private mutating func loadFromCSV(path: String) {
        guard let content = try? String(contentsOfFile: path, encoding: .utf8) else {
            print("❌ Failed to read symbols.csv")
            loadCommonSymbols()
            return
        }
        
        let lines = content.components(separatedBy: .newlines)
        var symbolIds: [Int] = []
        var loadedCount = 0
        
        // First pass: collect all symbol IDs
        for line in lines {
            let components = line.components(separatedBy: ",")
            guard components.count >= 2 else { continue }
            
            if let symbolId = Int(components[0]),
               !components[1].isEmpty {
                symbolIds.append(symbolId)
                let latex = components[1]
                symbolIdToLatex[symbolId] = latex
                loadedCount += 1
            }
        }
        
        // Sort and create index mapping
        symbolIds.sort()
        for (idx, symbolId) in symbolIds.enumerated() {
            idxToSymbolId[idx] = symbolId
        }
        
        print("✅ Loaded \(loadedCount) symbol mappings from CSV")
        print("   Created index mapping: \(idxToSymbolId.count) indices")
    }
    
    private mutating func loadCommonSymbols() {
        // Common mathematical symbols as fallback
        // Note: This doesn't include index mapping, so it won't work correctly
        // It's just a fallback for LaTeX lookup
        symbolIdToLatex = [
            // Arrows
            59: "\\rightarrow",
            753: "\\Rightarrow",
            767: "\\Leftrightarrow",
            // Operators
            88: "\\sum",
            116: "\\Sigma",
            183: "\\int",
            574: "\\prod",
            513: "\\times",
            184: "\\cdot",
            524: "\\pm",
            // Relations
            185: "\\leq",
            186: "\\geq",
            698: "\\neq",
            603: "\\equiv",
            601: "\\approx",
            // Set theory
            191: "\\subseteq",
            888: "\\in",
            511: "\\cup",
            530: "\\cap",
            // Logic
            882: "\\forall",
            891: "\\exists",
            // Greek letters
            81: "\\pi",
            82: "\\alpha",
            87: "\\beta",
            89: "\\sigma",
            117: "\\gamma",
            150: "\\Gamma",
            151: "\\delta",
            152: "\\Delta",
            155: "\\theta",
            156: "\\Theta",
            162: "\\lambda",
            163: "\\Lambda",
            164: "\\mu",
            168: "\\Pi",
            180: "\\omega",
            181: "\\Omega",
            // Other
            182: "\\partial",
            944: "\\infty",
            950: "\\emptyset",
            951: "\\nabla",
            958: "\\neg",
            960: "\\sqrt{}",
            968: "\\square",
        ]
    }
    
    /// Convert model output index (0-368) to symbol ID
    func getSymbolId(fromIndex index: Int) -> Int? {
        return idxToSymbolId[index]
    }
    
    /// Get LaTeX command for a symbol ID
    func getLatexCommand(for symbolId: Int) -> String {
        if let latex = symbolIdToLatex[symbolId] {
            return latex
        }
        // Fallback: return symbol ID
        return "\\symbol_\(symbolId)"
    }
    
    /// Get LaTeX command directly from model index (convenience method)
    func getLatexCommand(fromIndex index: Int) -> String {
        guard let symbolId = getSymbolId(fromIndex: index) else {
            return "\\symbol_index_\(index)"
        }
        return getLatexCommand(for: symbolId)
    }
    
    /// Get ranked LaTeX candidates for a symbol ID
    func getRankedCandidates(for symbolId: Int) -> [LaTeXCandidate] {
        return symbolIdToCandidates[symbolId] ?? []
    }
    
    /// Get ranked LaTeX candidates from model index
    func getRankedCandidates(fromIndex index: Int) -> [LaTeXCandidate] {
        guard let symbolId = getSymbolId(fromIndex: index) else {
            return []
        }
        return getRankedCandidates(for: symbolId)
    }
}
