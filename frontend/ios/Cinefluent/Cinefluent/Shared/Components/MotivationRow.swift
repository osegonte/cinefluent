import SwiftUI

struct MotivationRow: View {
    let title: String
    let icon: String
    let color: Color
    let isSelected: Bool
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 16) {
                RoundedRectangle(cornerRadius: 8)
                    .fill(color.opacity(0.2))
                    .frame(width: 40, height: 40)
                    .overlay(
                        Image(systemName: icon)
                            .font(.system(size: 18, weight: .medium))
                            .foregroundColor(color)
                    )
                
                Text(title)
                    .font(.cinefluent.body)
                    .foregroundColor(.cinefluent.text)
                
                Spacer()
                
                // Checkbox
                RoundedRectangle(cornerRadius: 4)
                    .stroke(Color.cinefluent.textTertiary.opacity(0.3), lineWidth: 2)
                    .frame(width: 24, height: 24)
                    .overlay(
                        RoundedRectangle(cornerRadius: 4)
                            .fill(isSelected ? Color.cinefluent.primary : Color.clear)
                            .overlay(
                                Image(systemName: "checkmark")
                                    .font(.system(size: 14, weight: .bold))
                                    .foregroundColor(.white)
                                    .opacity(isSelected ? 1 : 0)
                            )
                    )
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
                                lineWidth: 2
                            )
                    )
            )
        }
    }
}
