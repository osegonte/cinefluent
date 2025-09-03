import SwiftUI

struct LoginView: View {
    @EnvironmentObject var coordinator: AppCoordinator
    let showRegister: () -> Void
    
    @State private var email = ""
    @State private var password = ""
    @State private var isLoading = false
    
    var body: some View {
        ZStack {
            Color.cinefluent.background
                .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 32) {
                    Spacer().frame(height: 60)
                    
                    VStack(spacing: 16) {
                        CinefluentLogo(size: 80)
                        
                        Text("Welcome Back")
                            .font(.cinefluent.title)
                            .foregroundColor(.cinefluent.text)
                        
                        Text("Sign in to continue your learning journey")
                            .font(.cinefluent.body)
                            .foregroundColor(.cinefluent.textSecondary)
                            .multilineTextAlignment(.center)
                    }
                    
                    VStack(spacing: 16) {
                        CustomTextField(
                            title: "Email",
                            text: $email,
                            placeholder: "Enter your email",
                            keyboardType: .emailAddress
                        )
                        
                        CustomTextField(
                            title: "Password",
                            text: $password,
                            placeholder: "Enter your password",
                            isSecure: true
                        )
                    }
                    
                    VStack(spacing: 16) {
                        PrimaryButton(
                            title: isLoading ? "Signing In..." : "SIGN IN",
                            action: loginUser,
                            isEnabled: isFormValid && !isLoading,
                            style: .primary
                        )
                        
                        PrimaryButton(
                            title: "Continue with Google",
                            action: signInWithGoogle,
                            style: .secondary
                        )
                        
                        Button("Forgot Password?") {
                            // TODO: Implement forgot password
                            print("Forgot password")
                        }
                        .font(.cinefluent.bodyMedium)
                        .foregroundColor(.cinefluent.primary)
                        .padding(.top, 8)
                        
                        Button(action: showRegister) {
                            Text("Don't have an account? Sign Up")
                                .font(.cinefluent.bodyMedium)
                                .foregroundColor(.cinefluent.primary)
                        }
                        .padding(.top, 16)
                    }
                    
                    Spacer().frame(height: 40)
                }
                .padding(.horizontal, AppConstants.padding)
            }
        }
    }
    
    private var isFormValid: Bool {
        !email.isEmpty && !password.isEmpty
    }
    
    private func loginUser() {
        isLoading = true
        // TODO: Implement API call to your backend login endpoint
        print("Logging in user: \(email)")
        
        // Simulate API call
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isLoading = false
            // Existing users skip onboarding and go directly to main app
            coordinator.moveToMain()
        }
    }
    
    private func signInWithGoogle() {
        // TODO: Implement Google sign-in
        print("Sign in with Google")
        // For existing Google users, skip onboarding
        coordinator.moveToMain()
    }
}
