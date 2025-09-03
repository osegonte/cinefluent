import SwiftUI

extension Color {
    static let cinefluent = CinefluentColors()
}

struct CinefluentColors {
    let primary = Color(red: 0.76, green: 0.60, blue: 0.95)
    let primaryDark = Color(red: 0.66, green: 0.50, blue: 0.85)
    let primaryDeep = Color(red: 0.56, green: 0.40, blue: 0.87)
    
    let background = Color(red: 0.11, green: 0.13, blue: 0.18)
    let surface = Color(red: 0.16, green: 0.20, blue: 0.26)
    let card = Color(red: 0.20, green: 0.24, blue: 0.31)
    
    let text = Color.white
    let textSecondary = Color.white.opacity(0.8)
    let textTertiary = Color.white.opacity(0.6)
    
    let success = Color.green
    let warning = Color.orange
    let error = Color.red
    let info = Color.blue
}
