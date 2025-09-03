import SwiftUI

struct RegisterView: View {
    @EnvironmentObject var coordinator: AppCoordinator
    let showLogin: () -> Void
    
    @State private var name = ""
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
                        
                        Text("Create Account")
                            .font(.cinefluent.title)
                            .foregroundColor(.cinefluent.text)
                        
                        Text("Join millions learning languages through movies")
                            .font(.cinefluent.body)
                            .foregroundColor(.cinefluent.textSecondary)
                            .multilineTextAlignment(.center)
                    }
                    
                    VStack(spacing: 16) {
                        CustomTextField(
                            title: "Name",
                            text: $name,
                            placeholder: "Enter your name"
                        )
                        
                        CustomTextField(
                            title: "Email",
                            text: $email,
                            placeholder: "Enter your email",
                            keyboardType: .emailAddress
                        )
                        
                        CustomTextField(
                            title: "Password",
                            text: $password,
                            placeholder: "Create a password",
                            isSecure: true
                        )
                    }
                    
                    VStack(spacing: 16) {
                        PrimaryButton(
                            title: isLoading ? "Creating Account..." : "CREATE ACCOUNT",
                            action: registerUser,
                            isEnabled: isFormValid && !isLoading,
                            style: .primary
                        )
                        
                        PrimaryButton(
                            title: "Continue with Google",
                            action: signInWithGoogle,
                            style: .secondary
                        )
                        
                        Button(action: showLogin) {
                            Text("Already have an account? Sign In")
                                .font(.cinefluent.bodyMedium)
                                .foregroundColor(.cinefluent.primary)
                        }
                        .padding(.top, 8)
                    }
                    
                    Spacer().frame(height: 40)
                }
                .padding(.horizontal, AppConstants.padding)
            }
        }
    }
    
    private var isFormValid: Bool {
        !name.isEmpty && !email.isEmpty && !password.isEmpty && password.count >= 6
    }
    
    private func registerUser() {
        isLoading = true
        // TODO: Implement API call to your backend registration endpoint
        print("Registering user: \(name), \(email)")
        
        // Simulate API call
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isLoading = false
            // New users go through onboarding
            coordinator.moveToOnboarding()
        }
    }
    
    private func signInWithGoogle() {
        // TODO: Implement Google sign-in
        print("Sign in with Google")
        // For now, treat Google sign-in as new user (goes to onboarding)
        coordinator.moveToOnboarding()
    }
}
