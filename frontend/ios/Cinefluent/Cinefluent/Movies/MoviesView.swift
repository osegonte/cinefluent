import SwiftUI

struct MoviesView: View {
    var body: some View {
        NavigationView {
            ZStack {
                Color.cinefluent.background
                    .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 24) {
                        Text("Movies Library")
                            .font(.cinefluent.title)
                            .foregroundColor(.cinefluent.text)
                        
                        Text("Browse movies with subtitles for language learning")
                            .font(.cinefluent.body)
                            .foregroundColor(.cinefluent.textSecondary)
                            .multilineTextAlignment(.center)
                        
                        // Placeholder movie grid
                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 16) {
                            ForEach(1...6, id: \.self) { index in
                                MovieCard(title: "Movie \(index)")
                            }
                        }
                        .padding(.horizontal, AppConstants.padding)
                    }
                    .padding(.vertical, 40)
                }
            }
            .navigationTitle("Movies")
            .navigationBarHidden(true)
        }
    }
}

struct MovieCard: View {
    let title: String
    
    var body: some View {
        VStack(spacing: 12) {
            Rectangle()
                .fill(Color.cinefluent.surface)
                .frame(height: 120)
                .cornerRadius(12)
                .overlay(
                    Image(systemName: "play.circle.fill")
                        .font(.system(size: 40))
                        .foregroundColor(.cinefluent.primary)
                )
            
            Text(title)
                .font(.cinefluent.bodyMedium)
                .foregroundColor(.cinefluent.text)
        }
        .padding(16)
        .background(Color.cinefluent.card)
        .cornerRadius(AppConstants.cornerRadius)
    }
}

#Preview {
    MoviesView()
}
