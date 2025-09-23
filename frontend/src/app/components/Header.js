export default function Header({ activeSection, setActiveSection, sections }) {
  return (
    <header className="bg-white/10 backdrop-blur-lg border-b border-white/20 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
              JobMailer Pro
            </div>
            <div className="hidden md:block text-sm text-gray-300">
              AI-Powered Applications
            </div>
          </div>
          <nav className="flex space-x-2">
            {sections.map((section, index) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`px-4 py-2 rounded-lg transition-all duration-300 flex items-center space-x-2 ${
                  activeSection === section.id
                    ? 'bg-white/20 text-white shadow-lg'
                    : 'text-gray-300 hover:text-white hover:bg-white/10'
                }`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <span className="text-lg">{section.icon}</span>
                <span className="hidden sm:block font-medium">{section.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
