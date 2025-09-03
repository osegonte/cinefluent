import SwiftUI

enum OnboardingStep {
    case nativeLanguage
    case targetLanguage
    case skillLevel
    case motivation
    case dailyGoal
    case courseBuilding
}

struct OnboardingFlow: View {
    @EnvironmentObject var coordinator: AppCoordinator
    @State private var currentStep: OnboardingStep = .nativeLanguage
    @State private var selectedNativeLanguage = ""
    @State private var selectedTargetLanguage = ""
    @State private var selectedSkillLevel = ""
    @State private var selectedMotivations: Set<String> = []
    @State private var selectedDailyGoal = ""
    
    var body: some View {
        Group {
            switch currentStep {
            case .nativeLanguage:
                NativeLanguageView(
                    selectedLanguage: $selectedNativeLanguage,
                    onContinue: { currentStep = .targetLanguage },
                    onBack: { coordinator.moveToAuthentication() }
                )
            case .targetLanguage:
                TargetLanguageView(
                    nativeLanguage: selectedNativeLanguage,
                    selectedLanguage: $selectedTargetLanguage,
                    onContinue: { currentStep = .skillLevel },
                    onBack: { currentStep = .nativeLanguage }
                )
            case .skillLevel:
                SkillLevelView(
                    targetLanguage: selectedTargetLanguage,
                    selectedLevel: $selectedSkillLevel,
                    onContinue: { currentStep = .motivation },
                    onBack: { currentStep = .targetLanguage }
                )
            case .motivation:
                MotivationView(
                    targetLanguage: selectedTargetLanguage,
                    selectedMotivations: $selectedMotivations,
                    onContinue: { currentStep = .dailyGoal },
                    onBack: { currentStep = .skillLevel }
                )
            case .dailyGoal:
                DailyGoalView(
                    selectedGoal: $selectedDailyGoal,
                    onContinue: { currentStep = .courseBuilding },
                    onBack: { currentStep = .motivation }
                )
            case .courseBuilding:
                CourseBuildingView(
                    targetLanguage: selectedTargetLanguage,
                    onComplete: { coordinator.moveToMain() }
                )
            }
        }
        .animation(.easeInOut(duration: 0.3), value: currentStep)
    }
}
