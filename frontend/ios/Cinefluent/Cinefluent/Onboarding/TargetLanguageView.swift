import SwiftUI

struct TargetLanguageView: View {
    let nativeLanguage: String
    @Binding var selectedLanguage: String
    let onContinue: () -> Void
    let onBack: () -> Void
    
    private let languages = [
        ("en", "English", "🇺🇸"),
        ("es", "Spanish", "🇪🇸"),
        ("fr", "French", "🇫🇷"),
        ("de", "German", "🇩🇪"),
        ("it", "Italian", "🇮🇹"),
        ("pt", "Portuguese", "🇵🇹"),
        ("ja", "Japanese", "🇯🇵"),
        ("ko", "Korean", "🇰🇷"),
        ("zh", "Chinese", "🇨🇳"),
        ("ru", "Russian", "🇷🇺")
    ]
    
    private var filteredLanguages: [(String, String, String)] {
        languages.filter { $0.0 != nativeLanguage }
    }
    
    private var nativeLanguageName: String {
        languages.first(where: { $0.0 == nativeLanguage })?.1 ?? "English"
    }
    
    var body: some View {
        OnboardingPageLayout(
            progress: 0.32,
            title: "What would you like to learn?",
            subtitle: "For \(nativeLanguageName) speakers",
            onBack: onBack
        ) {
            LazyVStack(spacing: 12) {
                ForEach(filteredLanguages, id: \.0) { code, name, flag in
                    LanguageSelectionRow(
                        flag: flag,
                        name: name,
                        isSelected: selectedLanguage == code
                    ) {
                        selectedLanguage = code
                        onContinue()
                    }
                }
            }
        }
    }
}
