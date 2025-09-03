import SwiftUI

extension Font {
    static let cinefluent = CinefluentFonts()
}

struct CinefluentFonts {
    let largeTitle = Font.system(size: 48, weight: .bold, design: .rounded)
    let title = Font.system(size: 28, weight: .bold)
    let title2 = Font.system(size: 22, weight: .bold)
    let title3 = Font.system(size: 20, weight: .semibold)
    
    let body = Font.system(size: 17, weight: .regular)
    let bodyMedium = Font.system(size: 17, weight: .medium)
    let bodySemibold = Font.system(size: 17, weight: .semibold)
    
    let button = Font.system(size: 17, weight: .bold)
    let caption = Font.system(size: 14, weight: .regular)
    let footnote = Font.system(size: 12, weight: .regular)
}
