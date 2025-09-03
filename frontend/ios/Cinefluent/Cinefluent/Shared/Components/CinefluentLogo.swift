import SwiftUI

struct CinefluentLogo: View {
    let size: CGFloat
    
    var body: some View {
        ZStack {
            RoundedRectangle(cornerRadius: size * 0.28)
                .fill(
                    LinearGradient(
                        colors: [Color.cinefluent.primaryDeep, Color.cinefluent.primaryDark],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: size * 0.85, height: size * 0.85)
                .overlay(
                    Triangle()
                        .fill(Color.white)
                        .frame(width: size * 0.3, height: size * 0.3)
                        .offset(x: size * 0.03)
                )
                .offset(x: size * 0.15, y: size * 0.15)
                .shadow(color: Color.black.opacity(0.2), radius: size * 0.08, x: 0, y: size * 0.06)
            
            RoundedRectangle(cornerRadius: size * 0.28)
                .fill(
                    LinearGradient(
                        colors: [Color.cinefluent.primary, Color.cinefluent.primaryDark],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .frame(width: size * 0.85, height: size * 0.85)
                .overlay(
                    Text("文")
                        .font(.system(size: size * 0.4, weight: .medium))
                        .foregroundColor(.white)
                )
                .offset(x: -size * 0.15, y: -size * 0.15)
                .shadow(color: Color.black.opacity(0.15), radius: size * 0.06, x: 0, y: size * 0.04)
        }
        .frame(width: size, height: size)
    }
}

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.minX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.midY))
        path.closeSubpath()
        return path
    }
}
