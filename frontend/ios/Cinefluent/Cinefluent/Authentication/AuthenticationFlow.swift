import SwiftUI

enum AuthPage {
    case register
    case login
}

struct AuthenticationFlow: View {
    @EnvironmentObject var coordinator: AppCoordinator
    @State private var currentPage: AuthPage = .register
    
    var body: some View {
        Group {
            switch currentPage {
            case .register:
                RegisterView(showLogin: { currentPage = .login })
            case .login:
                LoginView(showRegister: { currentPage = .register })
            }
        }
        .animation(.easeInOut(duration: 0.3), value: currentPage)
    }
}
