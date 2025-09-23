export default function Footer() {
  return (
    <footer className="bg-white/5 backdrop-blur-lg border-t border-white/20 py-12 mt-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="animate-fadeIn">
            <h3 className="text-xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
              JobMailer Pro
            </h3>
            <p className="text-gray-300 leading-relaxed">
              Professional AI-powered job application platform. Create stunning emails and cover letters with ease.
            </p>
          </div>
          <div className="animate-fadeIn animation-delay-200">
            <h3 className="text-lg font-semibold mb-4 text-white">Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-center hover:text-white transition-colors cursor-pointer">
                <span className="mr-2">✨</span>
                AI Email Generation
              </li>
              <li className="flex items-center hover:text-white transition-colors cursor-pointer">
                <span className="mr-2">📄</span>
                Cover Letter PDFs
              </li>
              <li className="flex items-center hover:text-white transition-colors cursor-pointer">
                <span className="mr-2">🚀</span>
                Complete Workflow
              </li>
              <li className="flex items-center hover:text-white transition-colors cursor-pointer">
                <span className="mr-2">👤</span>
                Profile Management
              </li>
            </ul>
          </div>
          <div className="animate-fadeIn animation-delay-400">
            <h3 className="text-lg font-semibold mb-4 text-white">Technology</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-center">
                <span className="mr-2">⚡</span>
                Next.js 15.5.3
              </li>
              <li className="flex items-center">
                <span className="mr-2">🤖</span>
                Google Gemini AI
              </li>
              <li className="flex items-center">
                <span className="mr-2">🎨</span>
                Tailwind CSS
              </li>
              <li className="flex items-center">
                <span className="mr-2">🔧</span>
                Django REST API
              </li>
            </ul>
          </div>
        </div>
        <div className="border-t border-white/20 mt-12 pt-8 text-center">
          <p className="text-gray-400">
            &copy; 2024 JobMailer Pro. Built with ❤️ using modern web technologies.
          </p>
        </div>
      </div>
    </footer>
  );
}
