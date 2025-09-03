import SwiftUI

struct CustomTextField: View {
    let title: String
    @Binding var text: String
    let placeholder: String
    var keyboardType: UIKeyboardType = .default
    var isSecure: Bool = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.cinefluent.bodyMedium)
                .foregroundColor(.cinefluent.textSecondary)
            
            Group {
                if isSecure {
                    SecureField(placeholder, text: $text)
                } else {
                    TextField(placeholder, text: $text)
                        .keyboardType(keyboardType)
                        .autocapitalization(keyboardType == .emailAddress ? .none : .words)
                        .disableAutocorrection(keyboardType == .emailAddress)
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 16)
            .background(Color.cinefluent.surface)
            .foregroundColor(.cinefluent.text)
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.cinefluent.textTertiary.opacity(0.2), lineWidth: 1)
            )
        }
    }
}
