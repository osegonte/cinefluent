import SwiftUI

struct CourseBuildingView: View {
    let targetLanguage: String
    let onComplete: () -> Void
    @State private var logoScale: CGFloat = 1.0
    
    var body: some View {
        ZStack {
            Color.cinefluent.background.ignoresSafeArea()
            
            VStack(spacing: 40) {
                Spacer()
                
                VStack(spacing: 20) {
                    CinefluentLogo(size: 120)
                        .scaleEffect(logoScale)
                        .animation(
                            Animation.easeInOut(duration: 2.0)
                                .repeatForever(autoreverses: true),
                            value: logoScale
                        )
                    
                    Text("COURSE BUILDING...")
                        .font(.cinefluent.bodyMedium)
                        .foregroundColor(.cinefluent.textTertiary)
                        .tracking(1.5)
                    
                    Text("Get ready to join millions of people learning \(targetLanguage) with Cinefluent!")
                        .font(.cinefluent.title3)
                        .foregroundColor(.cinefluent.text)
                        .multilineTextAlignment(.center)
                }
                .padding(.horizontal, 40)
                
                Spacer()
            }
        }
        .onAppear {
            logoScale = 1.1
            DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                onComplete()
            }
        }
    }
}
