import SwiftUI

struct DashboardView: View {
    var body: some View {
        NavigationView {
            ZStack {
                Color.cinefluent.background
                    .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 24) {
                        // Welcome section
                        VStack(alignment: .leading, spacing: 16) {
                            HStack {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text("Welcome back!")
                                        .font(.cinefluent.title2)
                                        .foregroundColor(.cinefluent.text)
                                    
                                    Text("Ready to continue learning?")
                                        .font(.cinefluent.body)
                                        .foregroundColor(.cinefluent.textSecondary)
                                }
                                Spacer()
                                CinefluentLogo(size: 60)
                            }
                            .padding(AppConstants.cardPadding)
                            .background(Color.cinefluent.card)
                            .cornerRadius(AppConstants.cornerRadius)
                        }
                        
                        // Continue learning card
                        VStack(alignment: .leading, spacing: 16) {
                            Text("Continue Learning")
                                .font(.cinefluent.title3)
                                .foregroundColor(.cinefluent.text)
                            
                            HStack {
                                VStack(alignment: .leading, spacing: 8) {
                                    Text("Spanish Vocabulary")
                                        .font(.cinefluent.bodyMedium)
                                        .foregroundColor(.cinefluent.text)
                                    
                                    Text("Progress: 75%")
                                        .font(.cinefluent.caption)
                                        .foregroundColor(.cinefluent.textSecondary)
                                    
                                    ProgressView(value: 0.75)
                                        .tint(Color.cinefluent.primary)
                                }
                                
                                Spacer()
                                
                                Button("Resume") {
                                    print("Resume learning")
                                }
                                .font(.cinefluent.bodyMedium)
                                .foregroundColor(.white)
                                .padding(.horizontal, 16)
                                .padding(.vertical, 8)
                                .background(Color.cinefluent.primary)
                                .cornerRadius(8)
                            }
                        }
                        .padding(AppConstants.cardPadding)
                        .background(Color.cinefluent.card)
                        .cornerRadius(AppConstants.cornerRadius)
                        
                        // Stats section
                        VStack(alignment: .leading, spacing: 16) {
                            Text("Your Progress")
                                .font(.cinefluent.title3)
                                .foregroundColor(.cinefluent.text)
                            
                            HStack(spacing: 16) {
                                StatCard(title: "Streak", value: "7 days")
                                StatCard(title: "Words", value: "142")
                                StatCard(title: "Lessons", value: "23")
                            }
                        }
                        
                        Spacer().frame(height: 100)
                    }
                    .padding(.horizontal, AppConstants.padding)
                }
            }
            .navigationTitle("Dashboard")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack(spacing: 8) {
            Text(value)
                .font(.cinefluent.title2)
                .foregroundColor(.cinefluent.text)
            
            Text(title)
                .font(.cinefluent.caption)
                .foregroundColor(.cinefluent.textSecondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 16)
        .background(Color.cinefluent.surface)
        .cornerRadius(12)
    }
}

#Preview {
    DashboardView()
}
