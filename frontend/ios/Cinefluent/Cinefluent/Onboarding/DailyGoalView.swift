import SwiftUI

struct DailyGoalView: View {
    @Binding var selectedGoal: String
    let onContinue: () -> Void
    let onBack: () -> Void
    
    private let dailyGoals = [
        ("casual", "Casual", "5 min/day"),
        ("regular", "Regular", "10 min/day"),
        ("serious", "Serious", "15 min/day"),
        ("intense", "Intense", "20 min/day")
    ]
    
    var body: some View {
        OnboardingPageLayout(
            progress: 0.80,
            title: "How many minutes a day do you want to study?",
            onBack: onBack
        ) {
            LazyVStack(spacing: 12) {
                ForEach(dailyGoals, id: \.0) { id, title, description in
                    DailyGoalRow(
                        title: title,
                        description: description,
                        isSelected: selectedGoal == id
                    ) {
                        selectedGoal = id
                        onContinue()
                    }
                }
            }
        }
    }
}
