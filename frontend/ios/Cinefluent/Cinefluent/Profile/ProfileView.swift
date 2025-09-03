import SwiftUI

struct ProfileView: View {
    @EnvironmentObject var coordinator: AppCoordinator
    
    var body: some View {
        NavigationView {
            ZStack {
                Color.cinefluent.background
                    .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 32) {
                        // Profile header
                        VStack(spacing: 16) {
                            Circle()
                                .fill(Color.cinefluent.primary)
                                .frame(width: 80, height: 80)
                                .overlay(
                                    Text("JD")
                                        .font(.cinefluent.title)
                                        .foregroundColor(.white)
                                )
                            
                            VStack(spacing: 4) {
                                Text("John Doe")
                                    .font(.cinefluent.title2)
                                    .foregroundColor(.cinefluent.text)
                                
                                Text("Learning Spanish")
                                    .font(.cinefluent.body)
                                    .foregroundColor(.cinefluent.textSecondary)
                            }
                        }
                        .padding(.top, 40)
                        
                        // Profile options
                        VStack(spacing: 0) {
                            ProfileRow(title: "Account Settings", icon: "person.circle")
                            ProfileRow(title: "Learning Goals", icon: "target")
                            ProfileRow(title: "Statistics", icon: "chart.bar")
                            ProfileRow(title: "Notifications", icon: "bell")
                            ProfileRow(title: "Help & Support", icon: "questionmark.circle")
                            ProfileRow(title: "About", icon: "info.circle")
                        }
                        .background(Color.cinefluent.card)
                        .cornerRadius(AppConstants.cornerRadius)
                        
                        // Logout button
                        Button("Sign Out") {
                            coordinator.logout()
                        }
                        .font(.cinefluent.bodyMedium)
                        .foregroundColor(.cinefluent.error)
                        .padding()
                        
                        Spacer().frame(height: 100)
                    }
                    .padding(.horizontal, AppConstants.padding)
                }
            }
            .navigationTitle("Profile")
            .navigationBarHidden(true)
        }
    }
}

struct ProfileRow: View {
    let title: String
    let icon: String
    
    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: icon)
                .font(.system(size: 20))
                .foregroundColor(.cinefluent.primary)
                .frame(width: 24)
            
            Text(title)
                .font(.cinefluent.body)
                .foregroundColor(.cinefluent.text)
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .font(.system(size: 14, weight: .medium))
                .foregroundColor(.cinefluent.textTertiary)
        }
        .padding(.horizontal, AppConstants.cardPadding)
        .padding(.vertical, 16)
        .contentShape(Rectangle())
        .onTapGesture {
            print("Tapped \(title)")
        }
    }
}

#Preview {
    ProfileView()
        .environmentObject(AppCoordinator())
}
