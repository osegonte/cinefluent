import SwiftUI

struct PrimaryButton: View {
    let title: String
    let action: () -> Void
    var isEnabled: Bool = true
    var style: ButtonStyle = .primary
    
    enum ButtonStyle {
        case primary, secondary, outline
    }
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.cinefluent.button)
                .foregroundColor(textColor)
                .frame(maxWidth: .infinity, minHeight: AppConstants.buttonHeight)
                .background(backgroundView)
                .cornerRadius(AppConstants.cornerRadius)
                .overlay(
                    RoundedRectangle(cornerRadius: AppConstants.cornerRadius)
                        .stroke(borderColor, lineWidth: borderWidth)
                )
        }
        .disabled(!isEnabled)
        .opacity(isEnabled ? 1.0 : 0.6)
    }
    
    @ViewBuilder
    private var backgroundView: some View {
        switch style {
        case .primary:
            LinearGradient(
                gradient: Gradient(colors: [Color.cinefluent.primary, Color.cinefluent.primaryDark]),
                startPoint: .top,
                endPoint: .bottom
            )
        case .secondary:
            Color.cinefluent.surface
        case .outline:
            Color.clear
        }
    }
    
    private var textColor: Color {
        switch style {
        case .primary: return .white
        case .secondary: return Color.cinefluent.text
        case .outline: return Color.cinefluent.primary
        }
    }
    
    private var borderColor: Color {
        switch style {
        case .primary: return .clear
        case .secondary: return .clear
        case .outline: return Color.cinefluent.primary
        }
    }
    
    private var borderWidth: CGFloat {
        style == .outline ? 2 : 0
    }
}
