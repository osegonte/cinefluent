import SwiftUI

struct DailyGoalRow: View {
    let title: String
    let description: String
    let isSelected: Bool
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 16) {
                RoundedRectangle(cornerRadius: 8)
                    .fill(Color.cinefluent.primary.opacity(0.2))
                    .frame(width: 40, height: 40)
                    .overlay(
                        Image(systemName: "clock.fill")
                            .font(.system(size: 18, weight: .medium))
                            .foregroundColor(Color.cinefluent.primary)
                    )
                
                VStack(alignment: .leading, spacing: 4) {
                    Text(title)
                        .font(.cinefluent.bodyMedium)
                        .foregroundColor(.cinefluent.text)
                    
                    Text(description)
                        .font(.cinefluent.caption)
                        .foregroundColor(.cinefluent.textSecondary)
                }
                
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
            )
        }
    }
}
