import SwiftUI

enum AppState {
    case splash
    case authentication
    case onboarding
    case main
}

class AppCoordinator: ObservableObject {
    @Published var currentState: AppState = .splash
    @Published var isLoggedIn = false
    @Published var hasCompletedOnboarding = false
    
    init() {
        checkAppState()
    }
    
    private func checkAppState() {
        currentState = .splash
    }
    
    func moveToAuthentication() {
        currentState = .authentication
    }
    
    func moveToOnboarding() {
        currentState = .onboarding
    }
    
    func moveToMain() {
        currentState = .main
    }
    
    func logout() {
        isLoggedIn = false
        hasCompletedOnboarding = false
        currentState = .authentication
    }
}
