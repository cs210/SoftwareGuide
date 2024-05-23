import React, { useState } from 'react';
import TeamInfo from "./TeamInfo";
import teamsJson from "./teams.json";

const TeamData = ({ categoryMap }) => {
    const [searchQuery, setSearchQuery] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [openSection, setOpenSection] = useState(null);
    const [selectedTeam, setSelectedTeam] = useState(null);


    const teams = teamsJson;

    const handleSearchChange = (e) => {
        const query = e.target.value;
        setSearchQuery(query);

        if (query.length > 0) {
            let filteredSuggestions = teams
                .flatMap(team => [team.teamName, ...team.teamMembers.split(', ')])
                .filter(item => item.toLowerCase().includes(query.toLowerCase()));
            // only want to show top 10 queries
            if (filteredSuggestions.length > 10) {
                filteredSuggestions = filteredSuggestions.slice(0,10)
            }

            setSuggestions(filteredSuggestions);
            setShowSuggestions(true);
        } else {
            setShowSuggestions(false);
        }
    };

    const handleSuggestionClick = (suggestion) => {
        setSearchQuery(suggestion);
        setShowSuggestions(false);

        const matchingTeam = teams.find(team => 
            team.teamName === suggestion || 
            team.teamMembers.split(', ').includes(suggestion)
        );

        if (matchingTeam) {
            setSelectedTeam(matchingTeam);
            setOpenSection(matchingTeam.categories[0]);
        }
    };

    const groupedTeams = teams.reduce((acc, team) => {
        const categories = team.categories;
        const sectionsAdded = new Set(); // Keep track of sections a team has been added to

        categories.forEach((category) => {
            const section = categoryMap[category]?.section;
            if (section !== undefined && !sectionsAdded.has(section)) {
                if (!acc[section]) {
                    acc[section] = [];
                }
                acc[section].push(team);
                sectionsAdded.add(section); // Mark this section as added
            }
    });

    return acc;
}, {});
 

    return (
        <div>
            <div className="relative m-4">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35M17.65 11.95A6.65 6.65 0 1 1 11.95 5.3a6.65 6.65 0 0 1 5.7 6.65z" />
                    </svg>
                </div>
                <input 
                    type="text" 
                    placeholder="Search by team name or member name..." 
                    value={searchQuery}
                    onChange={handleSearchChange}
                    className="pl-10 p-2 border border-gray-400 rounded w-full caret-blue-500 focus:outline-none focus:ring focus:border-sky-500 "
                />
            </div>
            {showSuggestions && (
                <ul className="suggestions-list m-4 p-4 border border-gray-400 rounded w-7/8 bg-white">
                    {suggestions.map((suggestion, index) => (
                        <li 
                            key={index} 
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="cursor-pointer p-2 hover:bg-gray-200"
                        >
                            {suggestion}
                        </li>
                    ))}
                </ul>
            )}

            {selectedTeam && (
                <div className="m-4 p-4 border border-gray-400 rounded w-7/8 bg-white">
                    <TeamInfo 
                        teamName={selectedTeam.teamName}
                        teamNum={selectedTeam.teamNum}
                        description={selectedTeam.description}
                        categories={selectedTeam.categories}
                        teamMembers={selectedTeam.teamMembers}
                        categoryMap={categoryMap}
                    />
                </div>
            )}

            {Object.keys(categoryMap).map((category, index) => {
                const section = categoryMap[category].section;
                const teamsInSection = groupedTeams[section] || [];
                
                if (teamsInSection.length === 0) return null; // Only show categories with filtered teams
                const section_num = parseInt(section, 10)

                return (
                    <details key={index} id={`section-${section_num}`} className="m-4 border-b-4 border-black p-4" open={openSection === category}>
                        <summary className={`text-3xl font-semibold text-gray-800 cursor-pointer`}>
                            {category}
                        </summary>
                        {teamsInSection.map((team, idx) => (
                            <TeamInfo 
                                key={idx}
                                teamName={team.teamName}
                                teamNum={team.teamNum}
                                description={team.description}
                                categories={team.categories}
                                teamMembers={team.teamMembers}
                                categoryMap={categoryMap}
                            />
                        ))}
                    </details>
                );
            })}
        </div>
    );
};

export default TeamData;

