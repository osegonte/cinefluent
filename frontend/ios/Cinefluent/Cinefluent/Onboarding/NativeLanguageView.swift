import SwiftUI

struct NativeLanguageView: View {
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
    
    var body: some View {
        OnboardingPageLayout(
            progress: 0.16,
            title: "What language do you speak?",
            onBack: onBack
        ) {
            LazyVStack(spacing: 12) {
                ForEach(languages, id: \.0) { code, name, flag in
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
