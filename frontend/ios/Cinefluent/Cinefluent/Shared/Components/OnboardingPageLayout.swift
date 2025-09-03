import SwiftUI

struct OnboardingPageLayout<Content: View>: View {
    let progress: Double
    let title: String
    let subtitle: String?
    let onBack: () -> Void
    let showContinueButton: Bool
    let onContinue: (() -> Void)?
    let content: Content
    
    init(
        progress: Double,
        title: String,
        subtitle: String? = nil,
        onBack: @escaping () -> Void,
        showContinueButton: Bool = false,
        onContinue: (() -> Void)? = nil,
        @ViewBuilder content: () -> Content
    ) {
        self.progress = progress
        self.title = title
        self.subtitle = subtitle
        self.onBack = onBack
        self.showContinueButton = showContinueButton
        self.onContinue = onContinue
        self.content = content()
    }
    
    var body: some View {
        ZStack {
            Color.cinefluent.background.ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Header with progress and back button
                VStack(spacing: 24) {
                    HStack {
                        Button(action: onBack) {
                            Image(systemName: "arrow.left")
                                .font(.system(size: 20, weight: .medium))
                                .foregroundColor(.cinefluent.text)
                        }
                        
                        GeometryReader { geometry in
                            ZStack(alignment: .leading) {
                                RoundedRectangle(cornerRadius: 8)
                                    .fill(Color.cinefluent.surface)
                                    .frame(height: 8)
                                
                                RoundedRectangle(cornerRadius: 8)
                                    .fill(
                                        LinearGradient(
                                            colors: [Color.cinefluent.primary, Color.cinefluent.primaryDark],
                                            startPoint: .leading,
                                            endPoint: .trailing
                                        )
                                    )
                                    .frame(width: geometry.size.width * progress, height: 8)
                            }
                        }
                        .frame(height: 8)
                        
                        Spacer().frame(width: 44)
                    }
                    .padding(.horizontal, 24)
                    .padding(.top, 16)
                    
                    // Mascot with speech bubble
                    HStack(alignment: .top, spacing: 16) {
                        CinefluentLogo(size: 80)
                            .shadow(color: Color.black.opacity(0.2), radius: 8, x: 0, y: 4)
                        
                        VStack(alignment: .leading, spacing: 4) {
                            Text(title)
                                .font(.cinefluent.bodyMedium)
                                .foregroundColor(.cinefluent.text)
                                .padding(.horizontal, 20)
                                .padding(.vertical, 16)
                                .background(Color.cinefluent.surface)
                                .cornerRadius(16)
                                .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: 2)
                            
                            // Speech bubble tail
                            Triangle()
                                .fill(Color.cinefluent.surface)
                                .frame(width: 12, height: 8)
                                .rotationEffect(.degrees(180))
                                .offset(x: 20, y: -4)
                        }
                        
                        Spacer()
                    }
                    .padding(.horizontal, 24)
                }
                
                // Subtitle if provided
                if let subtitle = subtitle {
                    HStack {
                        Text(subtitle)
                            .font(.cinefluent.title2)
                            .foregroundColor(.cinefluent.text)
                        Spacer()
                    }
                    .padding(.horizontal, 24)
                    .padding(.top, 40)
                    .padding(.bottom, 20)
                } else {
                    Spacer().frame(height: 40)
                }
                
                // Content
                ScrollView {
                    content
                        .padding(.horizontal, 24)
                }
                
                // Continue button for multi-select screens
                if showContinueButton {
                    PrimaryButton(
                        title: "CONTINUE",
                        action: { onContinue?() },
                        style: .primary
                    )
                    .padding(.horizontal, 24)
                    .padding(.bottom, 24)
                }
                
                Spacer().frame(height: 24)
            }
        }
    }
}
