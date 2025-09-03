import SwiftUI

struct SkillLevelRow: View {
    let title: String
    let bars: Int
    let isSelected: Bool
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 16) {
                // Skill bars
                HStack(spacing: 4) {
                    ForEach(0..<5, id: \.self) { index in
                        RoundedRectangle(cornerRadius: 2)
                            .fill(index < bars ? Color.cinefluent.primary : Color.cinefluent.textTertiary.opacity(0.3))
                            .frame(width: 8, height: 20)
                    }
                }
                
                Text(title)
                    .font(.cinefluent.body)
                    .foregroundColor(.cinefluent.text)
                    .multilineTextAlignment(.leading)
                
                Spacer()
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 20)
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
