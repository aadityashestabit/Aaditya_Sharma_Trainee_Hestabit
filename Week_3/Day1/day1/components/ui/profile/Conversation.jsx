import ConversationTile from "./ConversationTile";

export default function Conversation(){
    return (

        <div className="bg-white rounded-2xl max-w-sm max-h-110 h-full p-6 space-y-3 w-100 text-xs ">
            <h1 className="text-lg text-gray-600 font-bold">Conversations</h1>
            <ConversationTile
        image="/images/1_face.png"
        name="Esthera Jackson"
        message="Hi! I need info"
        />


        <ConversationTile
        image="/images/2_face.png"
        name="Esthera Jackson"
        message="Hi! I need info"
        />


        <ConversationTile
        image="/images/4_face.png"
        name="Esthera Jackson"
        message="Hi! I need info"
        />


        <ConversationTile
        image="/images/6_face.png"
        name="Esthera Jackson"
        message="Hi! I need info"
        />

        </div>
        
    )
}