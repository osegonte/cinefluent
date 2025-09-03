import SwiftUI

struct AppCoordinatorView: View {
    @EnvironmentObject var coordinator: AppCoordinator
    
    var body: some View {
        Group {
            switch coordinator.currentState {
            case .splash:
                SplashView()
            case .authentication:
                AuthenticationFlow()
            case .onboarding:
                OnboardingFlow()
            case .main:
                MainTabView()
            }
        }
        .animation(.easeInOut(duration: 0.3), value: coordinator.currentState)
    }
}
