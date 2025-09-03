import SwiftUI

struct SkillLevelView: View {
    let targetLanguage: String
    @Binding var selectedLevel: String
    let onContinue: () -> Void
    let onBack: () -> Void
    
    private let skillLevels = [
        ("beginner", "I'm new to this language", 1),
        ("basic", "I know some common words", 2),
        ("intermediate", "I can have basic conversations", 3),
        ("advanced", "I can talk about various topics", 4),
        ("expert", "I can discuss most topics in detail", 5)
    ]
    
    var body: some View {
        OnboardingPageLayout(
            progress: 0.48,
            title: "How much \(targetLanguage) do you know?",
            onBack: onBack
        ) {
            LazyVStack(spacing: 12) {
                ForEach(skillLevels, id: \.0) { id, title, bars in
                    SkillLevelRow(
                        title: title,
                        bars: bars,
                        isSelected: selectedLevel == id
                    ) {
                        selectedLevel = id
                        onContinue()
                    }
                }
            }
        }
    }
}
