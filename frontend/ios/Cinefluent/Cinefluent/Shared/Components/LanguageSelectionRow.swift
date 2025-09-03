import SwiftUI

struct LanguageSelectionRow: View {
    let flag: String
    let name: String
    let isSelected: Bool
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 16) {
                Text(flag)
                    .font(.system(size: 28))
                
                Text(name)
                    .font(.cinefluent.bodyMedium)
                    .foregroundColor(.cinefluent.text)
                
                Spacer()
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 18)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(isSelected ? Color.cinefluent.surface.opacity(0.8) : Color.cinefluent.surface)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(
                                isSelected ? Color.cinefluent.primary : Color.clear,
                                lineWidth: 3
                            )
                    )
                    .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: 2)
            )
        }
    }
}
