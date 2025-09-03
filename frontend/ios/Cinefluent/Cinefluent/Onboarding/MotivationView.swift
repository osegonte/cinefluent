import SwiftUI

struct MotivationView: View {
    let targetLanguage: String
    @Binding var selectedMotivations: Set<String>
    let onContinue: () -> Void
    let onBack: () -> Void
    
    private let motivations = [
        ("productive", "Spend time productively", "brain.head.profile", Color.pink),
        ("education", "Support my education", "book.closed", Color.red),
        ("travel", "Prepare for travel", "airplane", Color.blue),
        ("career", "Boost my career", "briefcase", Color.orange),
        ("fun", "Just for fun", "party.popper", Color.yellow),
        ("connect", "Connect with people", "person.2", Color.green),
        ("other", "Other", "ellipsis", Color.purple)
    ]
    
    var body: some View {
        OnboardingPageLayout(
            progress: 0.64,
            title: "Why are you learning \(targetLanguage)?",
            onBack: onBack,
            showContinueButton: !selectedMotivations.isEmpty,
            onContinue: onContinue
        ) {
            LazyVStack(spacing: 12) {
                ForEach(motivations, id: \.0) { id, title, icon, color in
                    MotivationRow(
                        title: title,
                        icon: icon,
                        color: color,
                        isSelected: selectedMotivations.contains(id)
                    ) {
                        if selectedMotivations.contains(id) {
                            selectedMotivations.remove(id)
                        } else {
                            selectedMotivations.insert(id)
                        }
                    }
                }
            }
        }
    }
}
