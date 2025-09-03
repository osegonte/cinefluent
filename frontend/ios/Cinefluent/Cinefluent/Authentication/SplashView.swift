import SwiftUI

struct SplashView: View {
    @EnvironmentObject var coordinator: AppCoordinator
    @State private var logoScale: CGFloat = 0.8
    @State private var titleOpacity: Double = 0.0
    @State private var buttonsOpacity: Double = 0.0
    
    var body: some View {
        ZStack {
            Color.cinefluent.background
                .ignoresSafeArea()
            
            VStack(spacing: 40) {
                Spacer()
                
                VStack(spacing: 24) {
                    CinefluentLogo(size: 120)
                        .scaleEffect(logoScale)
                        .animation(.spring(response: 0.8, dampingFraction: 0.6), value: logoScale)
                    
                    VStack(spacing: 8) {
                        Text("cinefluent")
                            .font(.cinefluent.largeTitle)
                            .foregroundColor(.cinefluent.text)
                            .opacity(titleOpacity)
                        
                        Text("Learn through movies.")
                            .font(.cinefluent.bodyMedium)
                            .foregroundColor(.cinefluent.textSecondary)
                            .opacity(titleOpacity)
                    }
                }
                
                Spacer()
                
                VStack(spacing: 16) {
                    PrimaryButton(
                        title: "GET STARTED",
                        action: { coordinator.moveToAuthentication() },
                        style: .primary
                    )
                    
                    PrimaryButton(
                        title: "I ALREADY HAVE AN ACCOUNT", 
                        action: { coordinator.moveToAuthentication() },
                        style: .outline
                    )
                }
                .padding(.horizontal, AppConstants.padding)
                .opacity(buttonsOpacity)
                
                Spacer()
            }
        }
        .onAppear {
            logoScale = 1.0
            titleOpacity = 1.0 
            buttonsOpacity = 1.0
        }
    }
}
